-- see https://docs.snowflake.com/en/sql-reference/functions/st_union

SELECT ST_UNION(
  TO_GEOGRAPHY('POINT(1 1)'),
  TO_GEOGRAPHY('LINESTRING(1 0, 1 2)')
);