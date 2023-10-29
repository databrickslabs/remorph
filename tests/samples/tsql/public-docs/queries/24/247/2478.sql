-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT CONVERT(BINARY(4), '0x4E616D65', 1) AS [Style 1, character to binary];