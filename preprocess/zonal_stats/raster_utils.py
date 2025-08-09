import pandas as pd
from exactextract import exact_extract
import ibis
from ibis import _

def get_raster_file(metric, index):
    mean_end_plant = '/vsicurl/https://minio.carlboettiger.info/public-ca30x30/CBN/Biodiversity_unique/Rarityweighted_endemic_plant_richness/endemicspecies_E_epsg3310.tif'
    mean_plant = '/vsicurl/https://minio.carlboettiger.info/public-ca30x30/CBN/Biodiversity_unique/Plant_richness/species_D.tif'
    pct_plant = '/vsicurl/https://minio.carlboettiger.info/public-ca30x30/CBN/Biodiversity_unique/Plant_richness/species_D_80percent_epsg3310.tif'
    pct_end_plant = '/vsicurl/https://minio.carlboettiger.info/public-ca30x30/CBN/Biodiversity_unique/Rarityweighted_endemic_plant_richness/endemicspecies_E_80percent_epsg3310.tif'
    if metric == 'mean':
        names = ['mean_plant_richness','mean_rarityweighted_endemic_plant_richness']
        rasters = [mean_plant, mean_end_plant]
    elif metric == 'overlap':
        names = ['pct_top_plant_richness','pct_rarityweighted_endemic_plant_richness']
        rasters = [pct_plant, pct_end_plant]
    return names[index], rasters[index]

def get_raster_stats(con, label, name, raster, metric, index):
    name, raster  = get_raster_file(metric, index)
    compute_raster_stats(con, label, name, raster, metric)
    return 
    
def compute_percentage_overlap(df, name):
    def extract_overlap(row):
        if 1 in row['unique']:
            idx = row['unique'].index(1)
            return round(row['frac'][idx], 6)
        return 0
    df[name] = df.apply(extract_overlap, axis=1)
    return df[['id', 'sub_id', name, 'acres']]

def compute_raster_stats(con, label, name, raster, metric = 'mean'):
    print(label)
    print(metric)
    print(name)
    url = f's3://public-ca30x30/CA_Nature/2024/Preprocessing/v3/subsets/split_habitat_climate/{label}_habitat_climate.parquet'
    if label in ['gap2','gap4']: #don't compute with tiny polygons (exactextract gets mad if you keep them)
        polys = con.read_parquet(url).rename(new_id = 'id').execute()
        small = polys[round(polys['acres'],10) ==0]
        a = ibis.memtable(small, name = 'tmp')
        exclude_ids = a.select('sub_id').distinct().execute()['sub_id'].to_list()
        polys = polys[~polys['sub_id'].isin(exclude_ids)]

    else:
        polys = con.read_parquet(url).rename(new_id = 'id').execute()
    polys = polys.set_crs('epsg:3310')

    if metric == 'mean':  
        out = exact_extract(raster, polys, [metric], include_cols=["new_id","sub_id","acres"])
        rows = [{'id': f['properties']['new_id'], 'sub_id': f['properties']['sub_id'], name: round(f['properties'][metric], 6),
                'acres': f['properties']['acres']} for f in out]
        stats = pd.DataFrame(rows)

    # computing the overlap of each unique parcel then computing the overlap of only 1's 
    elif metric == 'overlap':
        metrics = ['frac','unique']
        out = exact_extract(raster, polys, metrics, include_cols=["new_id","sub_id","acres"])
        rows = [{'id': f['properties']['new_id'], 'sub_id': f['properties']['sub_id'], 'frac': list(f['properties']['frac']),  
                 'unique': list(f['properties']['unique']),
                 'acres': f['properties']['acres']} for f in out]
        stats = compute_percentage_overlap(pd.DataFrame(rows), name)
    out = con.create_table('tmp', stats, overwrite = True)

    ##zeroing out tiny polygons 
    if label in ['gap2','gap4']: 
        excluded = con.read_parquet(url).filter(_.sub_id.isin(exclude_ids)).mutate(**{name: ibis.literal(0)})
        excluded = excluded.cast({name:"float64"}).select('sub_id','id',name,'acres')
        out = out.union(excluded)
    save_url = f's3://public-ca30x30/CA_Nature/2024/Preprocessing/v3/stats/{label}/{name}.parquet'
    out.to_parquet(save_url)
    return



