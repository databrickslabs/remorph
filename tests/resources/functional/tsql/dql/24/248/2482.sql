-- tsql sql:
WITH CustomerCTE AS ( SELECT CONVERT(CHAR(8), 0x4E616d65, 2) AS CustomerName ) SELECT CustomerName AS [Style 2, binary to character] FROM CustomerCTE
