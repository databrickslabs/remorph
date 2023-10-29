-- see https://docs.snowflake.com/en/sql-reference/functions/timediff

SELECT TIMEDIFF(MONTH, '2017-01-1', '2017-12-31') AS Months;