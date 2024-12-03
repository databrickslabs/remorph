--Query type: DDL
CREATE TABLE #tblEmployee
(
    EmplId INT IDENTITY(1, 1) PRIMARY KEY CLUSTERED,
    DeptId INT,
    Salary INT
);

WITH CTE_tblEmployee AS
(
    SELECT DeptId, Salary
    FROM (
        VALUES (1, 1000), (2, 2000)
    ) AS SubQuery(DeptId, Salary)
)

SELECT DeptId, Salary
FROM CTE_tblEmployee;
