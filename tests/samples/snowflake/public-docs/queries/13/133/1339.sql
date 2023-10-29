-- see https://docs.snowflake.com/en/sql-reference/data-types-geospatial

SELECT ST_AREA(border) as area_in_sq_degrees
  FROM world_countries_geom
  WHERE name = 'Germany';