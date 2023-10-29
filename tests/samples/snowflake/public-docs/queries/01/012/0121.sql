-- see https://docs.snowflake.com/en/sql-reference/functions/st_startpoint

ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
SELECT ST_STARTPOINT(TO_GEOMETRY('LINESTRING(1 1, 2 2, 3 3, 4 4)'));
