-- see https://docs.snowflake.com/en/sql-reference/functions/object_agg

SELECT object_agg(k, v) FROM objectagg_example GROUP BY g;
