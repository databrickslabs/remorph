-- see https://docs.snowflake.com/en/sql-reference/functions/st_makepolygon

SELECT ST_MAKEPOLYGON(
  TO_GEOMETRY('LINESTRING(0.0 0.0, 1.0 0.0, 1.0 2.0, 0.0 2.0, 0.0 0.0)')
  ) AS polygon;