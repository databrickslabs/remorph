--Query type: DQL
WITH EmployeeRoles AS (
    SELECT 'Manager' AS Role
    UNION ALL
    SELECT 'Director'
    UNION ALL
    SELECT 'Developer'
    UNION ALL
    SELECT 'Tester'
)
SELECT CHOOSE(3, Role) AS Result
FROM EmployeeRoles;
