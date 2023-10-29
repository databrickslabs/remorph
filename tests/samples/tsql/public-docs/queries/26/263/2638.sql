-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/isjson-transact-sql?view=sql-server-ver16

SELECT ISJSON('"test string"', SCALAR)