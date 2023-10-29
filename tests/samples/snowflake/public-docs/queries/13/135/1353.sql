-- see https://docs.snowflake.com/en/sql-reference/functions/st_coveredby

SELECT ST_COVEREDBY(g1, g2) 
    FROM geospatial_table_01;