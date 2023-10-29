-- see https://docs.snowflake.com/en/sql-reference/functions/st_collect

-- Scalar function:
SELECT ST_COLLECT(g1, g2) FROM geo3;