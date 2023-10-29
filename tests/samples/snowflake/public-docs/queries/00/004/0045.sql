-- see https://docs.snowflake.com/en/sql-reference/functions/st_transform

-- Set the output format to EWKT
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT
  ST_TRANSFORM(
    ST_GEOMFROMWKT('POINT(4.500212 52.161170)'),
    4326,
    28992
  ) AS transformed_geom;