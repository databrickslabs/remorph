-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d smalldatetime = '2009-09-11 12:42:12'
SELECT 'Input', @d;
SELECT 'Truncated to minute', DATETRUNC(minute, @d)
SELECT 'Truncated to second', DATETRUNC(second, @d);