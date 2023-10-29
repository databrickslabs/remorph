-- see https://docs.snowflake.com/en/sql-reference/functions/st_aswkt

select st_aswkt(g)
    from geospatial_table
    order by id;