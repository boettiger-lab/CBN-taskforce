import ibis
from ibis import _
import ibis.selectors as s
import ibis.expr.datatypes as dt
import os

def get_url(folder, file, bucket = 'public-ca30x30', base_folder = 'CBN', method = 'write'):
    if method == 'write':
        minio = 's3://'
    else:
        minio = 'https://minio.carlboettiger.info/'
    if base_folder is None:
        path = os.path.join(bucket,folder,file)
    else:
        path = os.path.join(bucket,base_folder,folder,file)
    url = minio+path
    return url

def get_vector_file(metric):
    # CBN vector data
    amph_richness = get_url('ACE_biodiversity/ACE_amphibian_richness','ACE_amphibian_richness_epsg3310.parquet')
    pct_amph_richness = get_url('ACE_biodiversity/ACE_amphibian_richness','ACE_amphibian_richness_80percent_epsg3310.parquet')
    
    reptile_richness = get_url('ACE_biodiversity/ACE_reptile_richness','ACE_reptile_richness_epsg3310.parquet')
    pct_reptile_richness = get_url('ACE_biodiversity/ACE_reptile_richness','ACE_reptile_richness_80percent_epsg3310.parquet')
    
    bird_richness = get_url('ACE_biodiversity/ACE_bird_richness','ACE_bird_richness_epsg3310.parquet')
    pct_bird_richness = get_url('ACE_biodiversity/ACE_bird_richness','ACE_bird_richness_80percent_epsg3310.parquet')
    
    mammal_richness = get_url('ACE_biodiversity/ACE_mammal_richness','ACE_mammal_richness_epsg3310.parquet')
    pct_mammal_richness = get_url('ACE_biodiversity/ACE_mammal_richness','ACE_mammal_richness_80percent_epsg3310.parquet')
    
    rare_amphibian_richness = get_url('ACE_biodiversity/ACE_rare_amphibian_richness','ACE_rare_amphibian_richness_epsg3310.parquet')
    pct_rare_amphibian_richness = get_url('ACE_biodiversity/ACE_rare_amphibian_richness','ACE_rare_amphibian_richness_95percent_epsg3310.parquet')
    
    rare_reptile_richness = get_url('ACE_biodiversity/ACE_rare_reptile_richness','ACE_rare_reptile_richness_epsg3310.parquet')
    pct_rare_reptile_richness = get_url('ACE_biodiversity/ACE_rare_reptile_richness','ACE_rare_reptile_richness_95percent_epsg3310.parquet')
    
    rare_bird_richness = get_url('ACE_biodiversity/ACE_rare_bird_richness','ACE_rare_bird_richness_epsg3310.parquet')
    pct_rare_bird_richness = get_url('ACE_biodiversity/ACE_rare_bird_richness','ACE_rare_bird_richness_95percent_epsg3310.parquet')
    
    rare_mammal_richness = get_url('ACE_biodiversity/ACE_rare_mammal_richness','ACE_rare_mammal_richness_epsg3310.parquet')
    pct_rare_mammal_richness = get_url('ACE_biodiversity/ACE_rare_mammal_richness','ACE_rare_mammal_richness_95percent_epsg3310.parquet')
    
    endemic_amphibian_richness = get_url('ACE_biodiversity/ACE_endemic_amphibian_richness','ACE_endemic_amphibian_richness_epsg3310.parquet')
    pct_endemic_amphibian_richness = get_url('ACE_biodiversity/ACE_endemic_amphibian_richness','ACE_endemic_amphibian_richness_95percent_epsg3310.parquet')
    
    endemic_reptile_richness = get_url('ACE_biodiversity/ACE_endemic_reptile_richness','ACE_endemic_reptile_richness_epsg3310.parquet')
    pct_endemic_reptile_richness = get_url('ACE_biodiversity/ACE_endemic_reptile_richness','ACE_endemic_reptile_richness_95percent_epsg3310.parquet')
    
    endemic_bird_richness = get_url('ACE_biodiversity/ACE_endemic_bird_richness','ACE_endemic_bird_richness_epsg3310.parquet')
    pct_endemic_bird_richness = get_url('ACE_biodiversity/ACE_endemic_bird_richness','ACE_endemic_bird_richness_95percent_epsg3310.parquet')
    
    endemic_mammal_richness = get_url('ACE_biodiversity/ACE_endemic_mammal_richness','ACE_endemic_mammal_richness_epsg3310.parquet')
    pct_endemic_mammal_richness = get_url('ACE_biodiversity/ACE_endemic_mammal_richness','ACE_endemic_mammal_richness_95percent_epsg3310.parquet')
    
    freshwater_richness = get_url('Freshwater_resources/Freshwater_species_richness','freshwater_species_richness_ds1197_epsg3310.parquet')
    pct_freshwater_richness = get_url('Freshwater_resources/Freshwater_species_richness','freshwater_species_richness_ds1197_80percent_epsg3310.parquet')
    
    wetlands = get_url('Freshwater_resources/Wetlands','CA_wetlands_epsg3310.parquet')
    fire = get_url('Climate_risks/Historical_fire_perimeters','calfire_2023_epsg3310.parquet')
    farmland = get_url('NBS_agriculture/Farmland_all/Farmland','Farmland_2018_epsg3310.parquet')
    grazing = get_url('NBS_agriculture/Farmland_all/Lands_suitable_grazing','Grazing_land_2018_epsg3310.parquet')
    DAC = get_url('Progress_data_new_protection/DAC','DAC_2022_epsg3310.parquet')
    low_income = get_url('Progress_data_new_protection/Low_income_communities','low_income_CalEnviroScreen4_epsg3310.parquet')
    
    pct_newly_protected = get_url('Progress_data_new_protection/Newly_counted_lands/dissolved','newly_protected_2024_union_epsg3310.parquet')
    pct_data_improvement = get_url('Progress_data_new_protection/Newly_counted_lands/dissolved','data_improvement_2024_union_epsg3310.parquet')
    pct_increased_management = get_url('Progress_data_new_protection/Newly_counted_lands/dissolved','increased_management_2024_union_epsg3310.parquet')

    if metric == 'mean':
        names = ['mean_amphibian_richness','mean_reptile_richness',
                 'mean_bird_richness','mean_mammal_richness',
                 'mean_rare_amphibian_richness','mean_rare_reptile_richness',
                 'mean_rare_bird_richness','mean_rare_mammal_richness',
                 'mean_endemic_amphibian_richness','mean_endemic_reptile_richness',
                 'mean_endemic_bird_richness','mean_endemic_mammal_richness',
                 'mean_freshwater_richness']
        
        vectors = [amph_richness, reptile_richness,
                   bird_richness, mammal_richness,
                   rare_amphibian_richness, rare_reptile_richness,
                   rare_bird_richness, rare_mammal_richness,
                   endemic_amphibian_richness,
                   endemic_reptile_richness,
                   endemic_bird_richness,
                   endemic_mammal_richness,
                   freshwater_richness]
        
        cols = ['NtvAmph','NtvRept','NtvBird','NtvMamm',
                'RarAmph','RarRept','RarBird','RarMamm',
                'AmphEndem','ReptEndem','BirdEndem','MammEndem',
                'Freshwater_Species_Count']
        
    elif metric == 'overlap':
        names = ['pct_top_amphibian_richness','pct_top_reptile_richness',
                 'pct_top_bird_richness','pct_top_mammal_richness',
                 'pct_rare_amphibian_richness','pct_rare_reptile_richness',
                 'pct_rare_bird_richness','pct_rare_mammal_richness',
                 'pct_endemic_amphibian_richness','pct_endemic_reptile_richness',
                 'pct_endemic_bird_richness','pct_endemic_mammal_richness',
                 'pct_top_freshwater_richness',
                 'pct_wetlands','pct_fire','pct_farmland','pct_grazing',
                 'pct_disadvantaged_community','pct_low_income_community',
                'pct_newly_protected','pct_data_improvement','pct_increased_management']
    
        vectors = [pct_amph_richness, pct_reptile_richness,
                    pct_bird_richness, pct_mammal_richness,
                    pct_rare_amphibian_richness, pct_rare_reptile_richness,
                    pct_rare_bird_richness, pct_rare_mammal_richness,
                    pct_endemic_amphibian_richness,
                    pct_endemic_reptile_richness,
                    pct_endemic_bird_richness,
                    pct_endemic_mammal_richness,
                    pct_freshwater_richness,
                    wetlands,
                    fire, farmland, grazing,
                    DAC, low_income,
                    pct_newly_protected,
                    pct_data_improvement,
                    pct_increased_management
                  ]
        cols = [None] * len(vectors)
    return names, vectors, cols 


def get_vector_stats(con, index, label, metric):
    names, vectors, cols = get_vector_file(metric)
    name = names[index]
    vector = vectors[index]
    col = cols[index]
    print(label)
    print(name)
    url = f's3://public-ca30x30/CA_Nature/2024/Preprocessing/v3/subsets/split_habitat_climate/{label}_habitat_climate.parquet'
    stats_url = f's3://public-ca30x30/CA_Nature/2024/Preprocessing/v3/stats/{label}/{name}.parquet'
    vector_stats = vector_vector_stats(con, url, vector, metric, col)
    vector_stats = vector_stats.rename(**{name: metric})
    return vector_stats, stats_url


# usage: t.mutate(geom_valid = ST_MakeValid(t.geom))
@ibis.udf.scalar.builtin
def ST_MakeValid(geom) -> dt.geometry:
 ...


def vector_vector_stats(con, base, data_layer, metric, col):
    print(f'metric: {metric}')
    print(f'column name: {col}')
    t1 = con.read_parquet(base).select(_.id, _.sub_id, _.geom)
    if metric == 'mean':
        t2 = con.read_parquet(data_layer).rename(value = col).select(_.geom, _.value)
    else:
        t2 = con.read_parquet(data_layer).select(_.geom)

    t1 = t1.mutate(geom = ST_MakeValid(_.geom))
    t2 = t2.mutate(geom = ST_MakeValid(_.geom))

    stats = (t1
        .left_join(t2, t1.geom.intersects(t2.geom))
        .group_by(t1.id, t1.sub_id, t1.geom)
            )
    if metric == 'overlap':
        stats = (stats.agg(overlap = (
                t1.geom.intersection(t2.geom).area() / t1.geom.area())
                .sum().coalesce(0).round(3) )) # overlap  
    elif metric == 'mean':
        stats = (stats.agg(mean=(
                (t1.geom.intersection(t2.geom).area() / t1.geom.area() * t2.value)
                .sum().coalesce(0).round(3))))
    else:
        print('Select a metric.')
        return 
    #####  for some ACE data, nonconserved areas don't get captured, so we assign it a 0
    ##### only used this for ACE data + nonconserved. 
    # left join to keep all sub_ids
    # non_overlapping = t1.anti_join(stats, 'sub_id')
    # zero rows for non-overlapping sub_ids
    # if metric == 'overlap':
    # zeros = (non_overlapping
    #          .mutate(overlap = 0)
    #          .cast({'overlap':'float64'})
    #         )
    # elif metric == 'mean':
    #     zeros = (non_overlapping
    #              .mutate(mean = 0)
    #              .cast({'mean':'float64'})
    #             )
    # stats = stats.union(zeros)
    return stats
    

