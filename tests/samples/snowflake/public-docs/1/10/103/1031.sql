select st_dimension(g) as dimension, st_aswkt(g)
    from geospatial_table_02
    order by dimension, id;