-- see https://docs.snowflake.com/en/sql-reference/functions/in

SELECT (4, 5, NULL) IN ( (4, 5, NULL), (7, 8, 9) ) AS RESULT;