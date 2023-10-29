-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datepart-transact-sql?view=sql-server-ver16

SELECT DATEPART (tzoffset, '2007-05-10  00:00:01.1234567 +05:10');