-- see https://docs.snowflake.com/en/sql-reference/functions/st_contains

SELECT ST_CONTAINS(poly, poly_inside),
      ST_CONTAINS(poly, poly),
      ST_CONTAINS(poly, line_on_boundary),
      ST_CONTAINS(poly, line_inside)
  FROM (SELECT
    TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))') AS poly,
    TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))') AS poly_inside,
    TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)') AS line_on_boundary,
    TO_GEOMETRY('LINESTRING(-2 0, 0 0, 0 1)') AS line_inside);