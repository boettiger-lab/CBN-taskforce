from utils import *
import re

def convert_h3(con, s3, folder, file, cols, zoom, group = None, base_folder = "CBN/"):
    """
    Driver function to convert geometries to h3.
    """
    cols = ", ".join(cols) if isinstance(cols, list) else cols
    if folder:
        bucket, path = info(folder, file, base_folder)
    else:
        bucket, path = info(None, file, None)
    path, file = os.path.split(path)
    name, ext = os.path.splitext(file)
    print(f"Processing: {name}")
    t_name = name.replace('-', '')

    if group:
        con.read_parquet(f"s3://{bucket}/{name}.parquet", table_name=t_name)
        print(f'Computing zoom level {zoom}, grouping the data based on {group}')
        compute_grouped(con, t_name, cols, zoom, group, path = f"{bucket}/{path}")
        (con.read_parquet(f"s3://{bucket}/hex/zoom{zoom}/group_{group}/**")
         .to_parquet(f"s3://{bucket}/hex/zoom{zoom}/{name}.parquet")
        )
        
    else:
        con.read_parquet(f"s3://{bucket}/{path}/{file}", table_name=t_name)
        print(f'Computing zoom level {zoom} without grouping.')
        save_path = f"s3://{bucket}/{path}/hex/zoom{zoom}/{name}.parquet"
        h3_from_geom(con, t_name, cols, save_path, zoom)
        

    
def h3_from_geom(con, name, cols, save_path, zoom):
    """
    Computes hexes directly from geometry.
    """
    con.raw_sql(f'''
    CREATE OR REPLACE TEMP TABLE t2 AS
    SELECT {cols},
           h3_polygon_wkt_to_cells_string(ST_Force2D(dump.geom), {zoom}) AS h{zoom}
    FROM (
        SELECT {cols}, UNNEST(ST_Dump(geom)) AS dump
        FROM {name}
    )
    ''')
    
    con.sql(f'''
        SELECT {cols}, UNNEST(h{zoom}) AS h{zoom},
        ST_GeomFromText(h3_cell_to_boundary_wkt(UNNEST(h{zoom}))) AS geom
        FROM t2
    ''').to_parquet(save_path)


def compute_grouped(con, name, cols, zoom, group, path):
    groups = con.table(name).select(group).distinct().execute()[group].tolist()
    chunk_size = 500
    # separate data by group
    for sub in groups:
        sub_name = f"{name}_{re.sub(r'\W+', '_', sub)}"
        offset = 0
        i = 0
        # chunk data within groups 
        while True:
            print(f'Processing group {sub_name} chunk {i} offset {offset}')
            chunk_name = f"{sub_name}_chunk{i}"
            con.raw_sql(f"""
                CREATE OR REPLACE TEMP TABLE {chunk_name} AS
                SELECT * FROM {name} 
                WHERE {group} = '{sub}'
                LIMIT {chunk_size} 
                OFFSET {offset}
            """)
            if con.sql(f"SELECT 1 FROM {chunk_name} LIMIT 1").execute().empty:
                break
            save_path = f"s3://{path}/hex/zoom{zoom}/group_{group}/{sub_name}_chunk{i}.parquet"
            h3_from_geom(con, chunk_name, cols, save_path, zoom)
            offset += chunk_size
            i += 1

            