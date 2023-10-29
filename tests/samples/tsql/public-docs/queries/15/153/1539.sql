-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d date= '0001-01-01 00:00:00';
SELECT DATETRUNC(week, @d);