-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SELECT * FROM table(RESULT_SCAN(LAST_QUERY_ID(-2)));