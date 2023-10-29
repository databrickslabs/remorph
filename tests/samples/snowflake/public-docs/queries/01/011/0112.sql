-- see https://docs.snowflake.com/en/sql-reference/functions/st_setsrid

ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT ST_SETSRID(TO_GEOMETRY('POINT(13 51)'), 4326);
