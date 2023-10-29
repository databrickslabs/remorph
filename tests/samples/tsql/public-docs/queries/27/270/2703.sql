-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/parse-transact-sql?view=sql-server-ver16

SELECT PARSE('Monday, 13 December 2010' AS datetime2 USING 'en-US') AS Result;