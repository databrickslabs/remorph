-- see https://docs.snowflake.com/en/sql-reference/functions/st_within

SELECT ST_WITHIN(g1, g2) 
    FROM geospatial_table_01;