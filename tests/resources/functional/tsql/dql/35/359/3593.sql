-- tsql sql:
WITH EmployeeCTE AS (
    SELECT 'Engineer' AS Title
    UNION ALL
    SELECT 'Manager' AS Title
    UNION ALL
    SELECT 'Analyst' AS Title
)
SELECT COUNT(DISTINCT Title)
FROM EmployeeCTE
