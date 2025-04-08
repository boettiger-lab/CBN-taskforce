from minio.error import S3Error
from cng.utils import *

import zipfile
import os
import subprocess

import geopandas as gpd
import ibis
from ibis import _

import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import numpy as np


def info(folder, file, bucket = "public-ca30x30", base_folder = 'CBN-data/'):
    """
    Extract minio path to upload/download data 
    """
    path = os.path.join(base_folder, folder, file)
    # path = os.path.join(folder, file)
    return bucket, path 
    
def download(s3, folder, file, file_name = None):
    """
    Downloading file from minio
    """
    if not file_name: 
        file_name = file
    bucket, path = info(folder, file)
    s3.fget_object(bucket, path ,file_name) 
    return

def upload(s3, folder, file):
    """
    Uploading file from minio
    """
    bucket, path = info(folder, file)
    s3.fput_object(bucket, path ,file) 
    return

def unzip(s3, folder, file):
    """
    Unzipping zip files 
    """
    download(s3, folder, file)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall()
    return 

# def process_vector(s3, folder, file, file_name = None, gdf = None, crs="EPSG:3310"):
def process_vector(s3, folder, file, file_name = None, gdf = None, crs="EPSG:4326"):
    """
    Driver function to process vectors 
    """
    if gdf is None:
        gdf = gpd.read_file(file)
    if gdf.crs != crs:
        gdf = gdf.to_crs(crs)
    if gdf.geometry.name != 'geom':
        gdf = gdf.rename_geometry('geom')
    if file_name:
        file = file_name
    # upload_parquet(folder, file, gdf)
    name, ext = os.path.splitext(file)
    parquet_file = f"{name}{'.parquet'}"
    gdf.to_parquet(parquet_file)
    upload(s3, folder, parquet_file)

    return gdf.drop('geom',axis = 1).columns.to_list()

def process_raster(s3, folder, file, file_name = None):
    """
    Driver function to process rasters 
    """
    if file_name:
        file = file_name
    # output_file = reproject_raster(file)
    # upload(s3, folder, output_file)
    # output_cog_file = make_cog(output_file)
    # upload(s3, folder, output_cog_file)
    # output_vector, cols  = make_vector(output_file)
    # upload(s3, folder, output_vector)

    name, ext = os.path.splitext(file)
    output_file = f"{name}_processed{ext}"

    output_cog_file = f"{name}_processed_COG{ext}"

    output_vector_file = f"{name}_processed.parquet"
    print(output_file)
    print(output_cog_file)
    print(output_vector_file)
    # Reproject raster
    if not exists_on_s3(s3, folder, output_file):
        output_file = reproject_raster(file)
        upload(s3, folder, output_file)
    else:
        print(f"{output_file} already exists on S3, skipping reprojection/upload.")

    # Make COG
    if not exists_on_s3(s3, folder, output_cog_file):
        output_cog_file = make_cog(output_file)
        upload(s3, folder, output_cog_file)
    else:
        print(f"{output_cog_file} already exists on S3, skipping COG conversion/upload.")

    # Vectorize raster
    if not exists_on_s3(s3, folder, output_vector_file):
        output_vector_file, cols = make_vector(output_file)
        upload(s3, folder, output_vector_file)
    else:
        print(f"{output_vector_file} already exists on S3, skipping vectorization/upload.")
        # We still need column names
        gdf = gpd.read_parquet(output_vector_file)
        cols = gdf.drop('geom', axis=1).columns.to_list()
    return cols
    
def reproject_raster(input_file, crs="EPSG:3310"):
    """
    Reproject rasters 
    """
    suffix = '_processed'
    name, ext = os.path.splitext(input_file)
    output_file = f"{name}{suffix}{ext}"
    command = [
        "gdalwarp",
        "-t_srs", crs,
        input_file,
        output_file 
        ]
    try:
        subprocess.run(command, check=True)
        print(f"Reprojection successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during reprojection: {e}")
    return output_file 

def make_cog(input_file, crs="EPSG:4326"):
    """
    Converting TIF to COGs
    """
    suffix = '_COG'
    name, ext = os.path.splitext(input_file)
    output_file = f"{name}{suffix}{ext}"
    command = [
        "gdalwarp",
        "-t_srs", crs,
        "-of", "COG",
        input_file,
        output_file 
        ]
    try:
        subprocess.run(command, check=True)
        print(f"Successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during processing: {e}")
    return output_file 

def make_vector(input_file, crs="EPSG:4326"):
    """
    Converting rasters to vector formats in order to convert to h3
    """
    name, ext = os.path.splitext(input_file)
    output_file = f"{name}.parquet"
    # Open raster
    with rasterio.open(input_file) as src:
        image = src.read(1)  # read first band
        mask = image != src.nodata  # mask out nodata
    
        results = (
            {"geom": shape(geom), "value": value}
            for geom, value in shapes(image, mask=mask, transform=src.transform)
        )
    
    gdf = gpd.GeoDataFrame.from_records(results)
    gdf.set_geometry('geom', inplace=True)
    gdf['id'] = np.arange(len(gdf))
    gdf.set_crs(src.crs, inplace=True)
    if gdf.crs != crs:
        gdf.to_crs(crs, inplace=True)

    gdf.to_parquet(output_file)
    print(gdf)
    return output_file, gdf.drop('geom',axis = 1).columns.to_list()

def filter_raster(s3, folder, file, percentile):
    """
    Helper function to filter rasteres 
    """
    with rasterio.open(file) as src:
        data = src.read(1)  # Read the first band
        profile = src.profile
    # mask no data values
    masked_data = np.ma.masked_equal(data, src.nodata)

    # compute percentile/threshold 
    p = np.percentile(masked_data.compressed(),percentile)
    filtered = np.where(data >= p, data, src.nodata)
    name, ext = os.path.splitext(file)
    new_file = f"{name}{'_'}{percentile}{'percentile'}{ext}"

    profile.update(dtype=rasterio.float64)
    with rasterio.open(new_file, "w", **profile) as dst:
        dst.write(filtered, 1)
    cols = process_raster(s3, folder, file)
    return cols


def convert_pmtiles(con, s3, folder, file):
    """
    Convert to PMTiles with tippecanoe 
    """
    name, ext = os.path.splitext(file)
    if ext != '.geojson':
            (con.read_parquet(file).execute().set_crs('epsg:3310')
             .to_crs('epsg:4326').to_file(name+'.geojson'))
    to_pmtiles(name+'.geojson', name+'.pmtiles', options = ['--extend-zooms-if-still-dropping'])
    upload(s3, folder, name+'.pmtiles')
    return

def exists_on_s3(s3, folder, file):
    """
    Check if a file exists on S3
    """
    bucket, path = info(folder, file)
    print(bucket)
    print(path)
    
    try:
        s3.stat_object(bucket, path)
        return True
    except S3Error:
        return False

