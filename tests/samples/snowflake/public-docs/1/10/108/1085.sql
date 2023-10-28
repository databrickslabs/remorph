select st_asgeojson(g)
    from geospatial_table
    order by id;