-- tsql sql:
WITH CustomerCTE AS (
    SELECT 'John' AS c_name, '123 Main St' AS c_address
    UNION ALL
    SELECT 'Jane' AS c_name, '456 Elm St' AS c_address
)
SELECT NEXT VALUE FOR Test.CountBy1 OVER (ORDER BY c_name) AS ListNumber, c_name, c_address
FROM CustomerCTE;
