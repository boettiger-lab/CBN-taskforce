import ibis
from ibis import _
import ibis.expr.datatypes as dt

@ibis.udf.scalar.builtin
def ST_IsEmpty(geom: dt.geometry) -> dt.boolean:
    return f"ST_IsEmpty({geom})"
    
def combine_habitat_and_climate(data1_url, data2_url, con):

    SQM_PER_ACRE = 4046.8564224
    t1 = con.read_parquet(data1_url).select(_.habitat_type, _.geom)
    t2 = con.read_parquet(data2_url).select(_.climate_zone, _.geom)

    # intersection areas: where habitat and climate overlap
    intersected = (
        t1.inner_join(t2, t1.geom.intersects(t2.geom))
        .select(
            habitat_type=t1.habitat_type,
            climate_zone=t2.climate_zone,
            geom=t1.geom.intersection(t2.geom).name("geom")
        )
        .filter(_.geom.is_valid())
        .mutate(acres=( _.geom.area() / SQM_PER_ACRE ).round(4))
    )

    # habitat only: subtract all overlapping climate from each habitat polygon
    overlapping_climate = (
        t1.cross_join(t2)
        .filter(t1.geom.intersects(t2.geom))
        .select(t2.geom)
        .aggregate(union_geom=_.geom.unary_union())
    )
    habitat_with_union = t1.cross_join(overlapping_climate)
    habitat_only = (
        habitat_with_union.select(
            habitat_type=_.habitat_type,
            climate_zone=ibis.literal("None").name("climate_zone"),
            geom=_.geom.difference(_.union_geom).name("geom")
        )
        .filter(_.geom.is_valid())
        .mutate(acres=( _.geom.area() / SQM_PER_ACRE ).round(4))
    )

    # climate only: subtract all overlapping habitat from each climate polygon
    overlapping_habitat = (
        t2.cross_join(t1)
        .filter(t2.geom.intersects(t1.geom))
        .select(t1.geom)
        .aggregate(union_geom=_.geom.unary_union())
    )
    climate_with_union = t2.cross_join(overlapping_habitat)
    climate_only = (
        climate_with_union.select(
            habitat_type=ibis.literal("None").name("habitat_type"),
            climate_zone=_.climate_zone,
            geom=_.geom.difference(_.union_geom).name("geom")
        )
        .filter(_.geom.is_valid())
        .mutate(acres=( _.geom.area() / SQM_PER_ACRE ).round(4))
    )

    # combine 
    result = intersected.union(habitat_only).union(climate_only)
    # result = result.filter(~ST_IsEmpty(_.geom))
    return result
