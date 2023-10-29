-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT CONVERT(CHAR(8), 0x4E616d65, 1) AS [Style 1, binary to character];