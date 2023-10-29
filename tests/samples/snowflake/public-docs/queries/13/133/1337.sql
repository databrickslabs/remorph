-- see https://docs.snowflake.com/en/sql-reference/functions/st_area

SELECT ST_AREA(TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')) AS area;