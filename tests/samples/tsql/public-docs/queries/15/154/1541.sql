-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d datetime = '2020-02-02 02:02:02.002';
SELECT 'Input', @d;
SELECT 'Truncated', DATETRUNC(millisecond, @d);