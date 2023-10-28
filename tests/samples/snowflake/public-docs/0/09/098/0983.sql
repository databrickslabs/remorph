SELECT ST_COVERS(poly, poly_inside),
       ST_COVERS(poly, poly),
       ST_COVERS(poly, line_on_boundary),
       ST_COVERS(poly, line_inside)
  FROM (SELECT TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))') AS poly,
               TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))') AS poly_inside,
               TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)') AS line_on_boundary,
               TO_GEOMETRY('LINESTRING(-2 0, 0 0, 0 1)') AS line_inside);