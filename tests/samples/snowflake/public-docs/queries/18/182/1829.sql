-- see https://docs.snowflake.com/en/sql-reference/functions-analytic

SELECT x AS X_COL, y AS Y_COL FROM t GROUP BY x, y;