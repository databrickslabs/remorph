-- tsql sql:
WITH EmployeeCTE AS (SELECT 'John' AS EmployeeName, 1 AS OrgLevel, 'Sales' AS Department)
SELECT CONVERT(VARCHAR(10), OrgLevel) AS Text_OrgNode, OrgLevel AS EmpLevel, *
FROM EmployeeCTE
WHERE OrgLevel = 1
