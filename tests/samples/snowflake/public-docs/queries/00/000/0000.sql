-- see https://docs.snowflake.com/en/sql-reference/functions/st_collect

-- Aggregate and then Collect:
SELECT ST_COLLECT(ST_COLLECT(g1), ST_COLLECT(g2)) FROM geo3;