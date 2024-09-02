--Query type: DML
WITH MyCTE AS (
    SELECT 1 AS DepartmentID, 'Sales' AS Name, 'Management' AS GroupName, '2022-01-01' AS ModifiedDate
    UNION ALL
    SELECT 2, 'Marketing', 'Management', '2022-01-02'
    UNION ALL
    SELECT 3, 'IT', 'Technical', '2022-01-03'
),
MyLinkedServer AS (
    SELECT *
    FROM (
        VALUES (1, 'Sales', 'Management', '2022-01-01'),
               (2, 'Marketing', 'Management', '2022-01-02'),
               (3, 'IT', 'Technical', '2022-01-03')
    ) AS MyLinkedServer(DepartmentID, Name, GroupName, ModifiedDate)
)
SELECT DepartmentID, Name, GroupName, ModifiedDate
INTO #Departments
FROM MyLinkedServer;

SELECT *
FROM #Departments;

-- REMORPH CLEANUP: DROP TABLE #Departments;