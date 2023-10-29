-- see https://docs.snowflake.com/en/sql-reference/functions/st_asewkb

select st_asewkb(g)
    from geospatial_table
    order by id;