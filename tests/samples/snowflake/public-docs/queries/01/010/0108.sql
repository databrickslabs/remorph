-- see https://docs.snowflake.com/en/sql-reference/functions/st_endpoint

ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKT';
SELECT ST_ENDPOINT(TO_GEOGRAPHY('LINESTRING(1 1, 2 2, 3 3, 4 4)'));
