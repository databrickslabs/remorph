-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SELECT $1 AS value FROM VALUES (1), (2), (3);


SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE value > 1;
