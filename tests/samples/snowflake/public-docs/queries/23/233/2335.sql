-- see https://docs.snowflake.com/en/sql-reference/functions/st_asewkt

select st_asewkt(g)
    from geospatial_table
    order by id;