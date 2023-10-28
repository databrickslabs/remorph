SELECT ST_CENTROID(
    TO_GEOGRAPHY(
        'GEOMETRYCOLLECTION(POLYGON((10 10, 10 20, 20 20, 20 10, 10 10)), LINESTRING(0 0, 0 -2), POINT(50 -50))'
    )
) as center_of_collection_with_polygons;