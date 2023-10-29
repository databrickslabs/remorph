-- see https://docs.snowflake.com/en/sql-reference/functions/date_trunc

SELECT TO_TIME('23:39:20.123') AS "TIME1",
       DATE_TRUNC('MINUTE', "TIME1") AS "TRUNCATED TO MINUTE";