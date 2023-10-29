-- see https://docs.snowflake.com/en/sql-reference/data-types-geospatial

SELECT ST_AREA(border) AS area_in_sq_meters
  FROM world_countries
  WHERE name = 'Germany';