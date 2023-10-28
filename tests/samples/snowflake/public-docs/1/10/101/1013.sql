SELECT
    g,
    ST_XMIN(g),
    ST_XMAX(g),
    ST_YMIN(g),
    ST_YMAX(g)
  FROM extreme_point_collection
  ORDER BY id;