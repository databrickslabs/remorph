SELECT ST_CENTROID(
    TO_GEOGRAPHY(
        'POLYGON((10 10, 10 20, 20 20, 20 10, 10 10))'
    )
) as center_of_polygon;