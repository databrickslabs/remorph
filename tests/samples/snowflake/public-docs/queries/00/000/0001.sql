-- see https://docs.snowflake.com/en/sql-reference/functions/st_collect

-- Aggregate function:
SELECT ST_COLLECT(g1), ST_COLLECT(g2) FROM geo3;