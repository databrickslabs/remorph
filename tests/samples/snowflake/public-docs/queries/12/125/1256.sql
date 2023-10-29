-- see https://docs.snowflake.com/en/sql-reference/functions/monthname

SELECT MONTHNAME(TO_TIMESTAMP('2015-04-03 10:00')) AS MONTH;
