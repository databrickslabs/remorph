-- see https://docs.snowflake.com/en/sql-reference/functions/st_transform

-- Set the output format to EWKT
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT
  ST_TRANSFORM(
    ST_GEOMFROMWKT('POINT(389866.35 5819003.03)', 32633),
    3857
  ) AS transformed_geom;