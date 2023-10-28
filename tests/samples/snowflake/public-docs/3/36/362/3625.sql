SELECT name FROM world_countries_geom WHERE
  ST_INTERSECTS(border,
    TO_GEOMETRY(
      'LINESTRING(13.4814 52.5015, -121.8212 36.8252)'
    ));