SELECT ST_AREA(border) AS area_in_sq_meters
  FROM world_countries
  WHERE name = 'Germany';