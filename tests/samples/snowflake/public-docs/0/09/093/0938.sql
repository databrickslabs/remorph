SELECT ST_PERIMETER(g), ST_ASWKT(g)
FROM (SELECT TO_GEOMETRY(column1) AS g
  FROM VALUES ('POINT(1 1)'),
              ('LINESTRING(0 0, 1 1)'),
              ('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))'));