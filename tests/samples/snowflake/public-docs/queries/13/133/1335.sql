-- see https://docs.snowflake.com/en/sql-reference/functions/st_makepolygonoriented

SELECT ST_AREA(
  ST_MAKEPOLYGONORIENTED(
    TO_GEOGRAPHY('LINESTRING(0.0 0.0, 0.0 2.0, 1.0 2.0, 1.0 0.0, 0.0 0.0)')
  )
) AS area_of_polygon;
