-- see https://docs.snowflake.com/en/sql-reference/functions/st_aswkb

select st_aswkb(g)
    from geospatial_table
    order by id;