-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SELECT $1 AS output_col FROM table(RESULT_SCAN(LAST_QUERY_ID()));