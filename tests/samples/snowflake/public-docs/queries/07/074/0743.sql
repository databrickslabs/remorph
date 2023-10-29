-- see https://docs.snowflake.com/en/sql-reference/functions/st_ymin

SELECT
    g,
    ST_XMIN(g),
    ST_XMAX(g),
    ST_YMIN(g),
    ST_YMAX(g)
  FROM extreme_point_collection
  ORDER BY id;