-- see https://docs.snowflake.com/en/sql-reference/functions/st_dimension

select st_dimension(g) as dimension, st_aswkt(g)
    from geospatial_table_02
    order by dimension, id;