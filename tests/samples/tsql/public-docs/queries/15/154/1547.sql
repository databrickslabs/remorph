-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d time = '12:12:12.1234567';
SELECT DATETRUNC(year, @d);