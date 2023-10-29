-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d datetime2 = '1998-12-11 02:03:04.1234567';
SELECT DATETRUNC(day, @d);