-- see https://docs.snowflake.com/en/sql-reference/functions/st_geometryfromwkt

-- Set the output format to EWKT
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT ST_GEOMETRYFROMEWKT('SRID=32633;POINT(389866.35 5819003.03)');