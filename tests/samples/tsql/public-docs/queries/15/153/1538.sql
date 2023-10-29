-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d date = '2050-04-04';
SELECT 'Input', @d;
SELECT 'Truncated', DATETRUNC(day, @d);