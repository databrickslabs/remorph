-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/trim-transact-sql?view=sql-server-ver16

SELECT TRIM(BOTH '123' FROM '123abc123') AS Result;