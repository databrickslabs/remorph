--Query type: DQL
WITH CustomerCTE AS (SELECT 'Customer Name' AS CustomerName)
SELECT CONVERT(BINARY(8), CustomerName, 0) AS [Style 0, character to binary]
FROM CustomerCTE
