-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d datetime2(3) = '2021-12-12 12:12:12.12345';
SELECT DATETRUNC(microsecond, @d);