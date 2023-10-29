-- see https://docs.snowflake.com/en/sql-reference/operators-query

SELECT v::VARCHAR FROM t1
UNION
SELECT i::VARCHAR FROM t2;