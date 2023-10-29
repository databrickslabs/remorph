-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SELECT PARSE_JSON(output_col) AS JSON_COL FROM table(RESULT_SCAN(LAST_QUERY_ID()));