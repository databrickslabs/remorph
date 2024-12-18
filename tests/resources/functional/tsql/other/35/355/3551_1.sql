-- tsql sql:
CREATE TABLE #Department
(
    DepartmentID INT,
    GroupName NVARCHAR(50)
);

INSERT INTO #Department (DepartmentID, GroupName)
VALUES
    (1, 'Sales'),
    (2, 'Marketing'),
    (3, 'IT'),
    (4, 'HR');

WITH DepartmentCTE AS
(
    SELECT DepartmentID, GroupName
    FROM #Department
)
UPDATE T
SET T.GroupName = N'Public Relations'
FROM DepartmentCTE T
WHERE T.DepartmentID = 4;

SELECT *
FROM #Department;

-- REMORPH CLEANUP: DROP TABLE #Department;
