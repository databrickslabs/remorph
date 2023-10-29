-- see https://docs.snowflake.com/en/sql-reference/functions/st_npoints

SELECT ST_NPOINTS(g1) 
    FROM geospatial_table_01;