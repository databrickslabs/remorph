-- see https://docs.snowflake.com/en/sql-reference/functions/st_perimeter

SELECT ST_PERIMETER(TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'));