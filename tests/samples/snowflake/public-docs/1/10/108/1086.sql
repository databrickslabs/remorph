select st_asgeojson(g)::varchar
    from geospatial_table
    order by id;