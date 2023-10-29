-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

--Convert the binary value 0x4E616d65 to a character value.
SELECT CONVERT(CHAR(8), 0x4E616d65, 0) AS [Style 0, binary to character];