-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d datetime = '2015-04-29 05:06:07.123';
SELECT 'Input', @d;
SELECT 'Truncated', DATETRUNC(millisecond, @d);