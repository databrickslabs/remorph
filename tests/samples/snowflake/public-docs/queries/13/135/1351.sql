-- see https://docs.snowflake.com/en/sql-reference/functions/st_contains

SELECT ST_CONTAINS(g1, g2) 
    FROM geospatial_table_01;