-- see https://docs.snowflake.com/en/sql-reference/functions/st_covers

SELECT ST_COVERS(g1, g2) 
    FROM geospatial_table_01;