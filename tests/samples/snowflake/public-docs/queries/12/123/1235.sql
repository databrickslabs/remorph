-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SELECT JSON_COL:keyB FROM table(RESULT_SCAN(LAST_QUERY_ID()));