-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datepart-transact-sql?view=sql-server-ver16

DECLARE @t time = '12:10:30.123';   
SELECT DATEPART(year, @t);