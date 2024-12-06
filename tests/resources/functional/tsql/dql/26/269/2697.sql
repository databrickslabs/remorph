-- tsql sql:
WITH EmployeeCTE AS (
    SELECT CAST(OrgNode AS VARCHAR(50)) AS OrgNode,
           OrgNode.GetLevel() AS EmpLevel,
           *
    FROM (
        VALUES (1, 'OrgNode1', 1),
               (2, 'OrgNode2', 2),
               (3, 'OrgNode3', 3)
    ) AS EmployeeDemo (EmployeeID, OrgNode, Level)
)
SELECT OrgNode.ToString() AS Text_OrgNode,
       EmpLevel,
       *
FROM EmployeeCTE
WHERE EmpLevel = 2;
