SELECT ST_MAKELINE(
  TO_GEOMETRY('LINESTRING(1.0 2.0, 10.1 5.5)'),
  TO_GEOMETRY('MULTIPOINT(3.5 4.5, 6.1 7.9)')) AS line_from_linestring_and_multipoint;