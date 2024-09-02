--Query type: DQL
WITH CustomerCTE AS ( SELECT CONVERT(CHAR(8), 0x4E616d65, 0) AS CustomerName ) SELECT CustomerName AS [Style 0, binary to character] FROM CustomerCTE