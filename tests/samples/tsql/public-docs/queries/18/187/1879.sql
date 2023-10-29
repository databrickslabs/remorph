-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

DECLARE @string VARCHAR(10);
SET @string = 1;
SELECT @string + ' is a string.' AS Result