-- see https://docs.snowflake.com/en/sql-reference/functions/st_makeline

SELECT ST_MAKELINE(
  TO_GEOMETRY('POINT(1.0 2.0)'),
  TO_GEOMETRY('POINT(3.5 4.5)')) AS line_between_two_points;