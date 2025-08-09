import ibis
from ibis import _

def get_ecoregion(index):
    ecoregions = ['Central_California_Coast',
     'Central_Valley_Coast_Ranges',
     'Colorado_Desert',
     'Great_Valley_North',
     'Great_Valley_South',
     'Klamath_Mountains',
     'Modoc_Plateau',
     'Mojave_Desert',
     'Mono',
     'Northern_California_Coast',
     'Northern_California_Coast_Ranges',
     'Northern_California_Interior_Coast_Ranges',
     'Northwestern_Basin_and_Range',
     'Sierra_Nevada',
     'Sierra_Nevada_Foothills',
     'Sonoran_Desert',
     'Southeastern_Great_Basin',
     'Southern_California_Coast',
     'Southern_California_Mountains_and_Valleys',
     'Southern_Cascades']
    eco = ecoregions[index]
    return eco

def split_layer(data3_url, con):
    overlap_url = 's3://public-ca30x30/CA_Nature/2024/Preprocessing/v3/Habitat_and_Climate_zones/CWHR13_climate_dissolved_geoms_simplify10m_includesNA.parquet'
    overlap_table = con.read_parquet(overlap_url)
    SQM_PER_ACRE = 4046.8564224
    t3 = con.read_parquet(data3_url).select("id", "name", "manager", "manager_type", "county", "gap_code",
                                            "status", "land_tenure", "ecoregion", "access_type", "geom")

    # append each id with the habitat + climate zone combo as its "sub_id" 
    habitat_letter_map = {
        "Agriculture": "a",
        "Barren/Other": "b",
        "Conifer Forest": "c",
        "Conifer Woodland": "d",
        "Desert Shrub": "e",
        "Desert Woodland": "f",
        "Hardwood Forest": "g",
        "Hardwood Woodland": "h",
        "Herbaceous": "i",
        "Shrub": "j",
        "Urban": "k",
        "Water": "l",
        "Wetland": "m",
        "None": "n"
    }

    climate_letter_map = {
        "Zone 1": "a",
        "Zone 2": "b",
        "Zone 3": "c",
        "Zone 4": "d",
        "Zone 5": "e",
        "Zone 6": "f",
        "Zone 7": "g",
        "Zone 8": "h",
        "Zone 9": "i",
        "Zone 10": "j",
        "None": "k",
    }

    habitat_letter_table = ibis.memtable([{"habitat_type": k, "habitat_letter": v} for k, v in habitat_letter_map.items()])
    climate_letter_table = ibis.memtable([{"climate_zone": k, "climate_letter": v} for k, v in climate_letter_map.items()])

    # join mappings to overlap table
    overlap_labeled = (
        overlap_table
        .inner_join(habitat_letter_table, "habitat_type")
        .inner_join(climate_letter_table, "climate_zone")
    )

    # cross join and spatial intersection
    joined = t3.cross_join(overlap_labeled)
    joined = joined.mutate(intersects=t3.geom.intersects(overlap_labeled.geom))

    # filter for intersection or include if no match (preserve unmatched)
    matched = joined.filter(joined.intersects)

    # calculate sub_id and geometry for matches
    matched = matched.select(
        id=t3.id,
        sub_id=t3.id.cast("string")
                .concat("_")
                .concat(overlap_labeled.habitat_letter)
                .concat(overlap_labeled.climate_letter)
                .name("sub_id"),
        habitat_type=overlap_labeled.habitat_type,
        climate_zone=overlap_labeled.climate_zone,
        name=t3.name,
        manager=t3.manager,
        manager_type=t3.manager_type,
        county=t3.county,
        gap_code=t3.gap_code,
        status=t3.status,
        land_tenure=t3.land_tenure,
        ecoregion=t3.ecoregion,
        access_type=t3.access_type,
        geom=t3.geom.intersection(overlap_labeled.geom),
        acres=(t3.geom.intersection(overlap_labeled.geom).area() / SQM_PER_ACRE).round(4)
    )

    # find unmatched records (no overlap)
    matched_ids = matched.select("id").distinct()
    
    # left join to find unmatched rows
    unmatched = t3.left_join(matched_ids, "id").filter(matched_ids.id.isnull())
    unmatched = unmatched.select(
        id=t3.id,
        sub_id=t3.id.cast("string").concat("_n").concat("k").name("sub_id"),
        habitat_type=ibis.literal("None"),
        climate_zone=ibis.literal("None"),
        name=t3.name,
        manager=t3.manager,
        manager_type=t3.manager_type,
        county=t3.county,
        gap_code=t3.gap_code,
        status=t3.status,
        land_tenure=t3.land_tenure,
        ecoregion=t3.ecoregion,
        access_type=t3.access_type,
        geom=t3.geom,
        acres=(t3.geom.area() / SQM_PER_ACRE).round(4)
    )
    
    # compute unmatched residuals by subtracting all intersected parts from each t3.geom
    matched_geoms = matched.group_by("id").aggregate(
        matched_union=matched.geom.unary_union()
)
    # join to get original geom
    residuals = t3.inner_join(matched_geoms, "id").mutate(
        residual_geom=t3.geom.difference(matched_geoms.matched_union)
    )
    # only keep meaningful residual geoms, not empty geoms.
    residuals = (residuals
                 .filter((_.residual_geom.is_valid()) 
                         & ((_.residual_geom.area()) > 0 )
                        ))
    
    # unmatched parts
    residual_rows = residuals.select(
        id=t3.id,
        sub_id=t3.id.cast("string").concat("_n").concat("k").name("sub_id"),
        habitat_type=ibis.literal("None"),
        climate_zone=ibis.literal("None"),
        name=t3.name,
        manager=t3.manager,
        manager_type=t3.manager_type,
        county=t3.county,
        gap_code=t3.gap_code,
        status=t3.status,
        land_tenure=t3.land_tenure,
        ecoregion=t3.ecoregion,
        access_type=t3.access_type,
        geom=_.residual_geom,
        acres=(_.residual_geom.area() / SQM_PER_ACRE).round(4)
    )
    result = matched.union(unmatched).union(residual_rows)
    return result

def check_results(con, url,save_url):
    original_id = con.read_parquet(url).select('id').distinct().execute()['id']
    new_id = con.read_parquet(save_url).select('id').distinct().execute()['id']
    missing_ids = list(set(original_id)- set(new_id))
    print(f'# of missing IDs: {len(missing_ids)}')
    original_acres = con.read_parquet(url).select('acres').execute()['acres'].sum()
    new_acres = con.read_parquet(save_url).select('acres').execute()['acres'].sum()
    acres_loss = original_acres-new_acres
    print(f'Acres loss: {acres_loss}\n')
    print(f'Ratio: {new_acres/original_acres}\n')
    return missing_ids
