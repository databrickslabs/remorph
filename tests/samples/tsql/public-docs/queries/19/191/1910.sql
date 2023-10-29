-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

DECLARE @x NVARCHAR(10) = 'ab' + NCHAR(0x10000);

SELECT CAST(@x AS NVARCHAR(3));