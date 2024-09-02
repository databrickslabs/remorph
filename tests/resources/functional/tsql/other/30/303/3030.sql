--Query type: DML
WITH HierarchyCTE AS (
    SELECT hierarchyid::GetRoot() AS id, 'Root' AS name
    UNION ALL
    SELECT hierarchyid::GetRoot().GetDescendant(NULL, NULL), 'Child 1'
    UNION ALL
    SELECT hierarchyid::GetRoot().GetDescendant(hierarchyid::GetRoot().GetDescendant(NULL, NULL), NULL), 'Child 2'
)
SELECT * FROM HierarchyCTE;