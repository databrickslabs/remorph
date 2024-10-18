--Query type: DQL
WITH ManagerCTE AS (
    SELECT CAST('/1/' AS hierarchyid) AS OrgNode
)
SELECT *
FROM (
    VALUES (
        CAST('/1/1/' AS hierarchyid)
    ), (
        CAST('/1/2/' AS hierarchyid)
    ), (
        CAST('/1/3/' AS hierarchyid)
    )
) AS EmployeeDemo(OrgNode)
WHERE OrgNode.IsDescendantOf((SELECT OrgNode FROM ManagerCTE)) = 1