-- see https://docs.snowflake.com/en/sql-reference/functions/st_makeline

SELECT ST_MAKELINE(
  TO_GEOMETRY('POINT(1.0 2.0)'),
  TO_GEOMETRY('MULTIPOINT(3.5 4.5, 6.1 7.9)')) AS line_from_point_and_multipoint;