-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

CALL return_JSON();
SELECT JSON_COL:keyB
        FROM (
             SELECT PARSE_JSON(RETURN_JSON::VARIANT) AS JSON_COL 
                 FROM table(RESULT_SCAN(LAST_QUERY_ID()))
             );