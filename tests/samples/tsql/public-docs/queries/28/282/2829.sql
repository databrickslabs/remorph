-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/try-parse-transact-sql?view=sql-server-ver16

SELECT TRY_PARSE('Jabberwokkie' AS datetime2 USING 'en-US') AS Result;