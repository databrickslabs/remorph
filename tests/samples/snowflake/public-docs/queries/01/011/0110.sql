-- see https://docs.snowflake.com/en/sql-reference/functions/st_pointn

ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKT';
SELECT ST_POINTN(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)'), 2);
