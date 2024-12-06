-- tsql sql:
WITH CustomerCTE AS (
    SELECT 'John' AS c_name, '123 Main St' AS c_address
    UNION ALL
    SELECT 'Alice', '456 Elm St'
    UNION ALL
    SELECT 'Bob', '789 Oak St'
)
SELECT TOP 5 c_name, c_address
FROM CustomerCTE
WHERE c_name LIKE 'A%';
