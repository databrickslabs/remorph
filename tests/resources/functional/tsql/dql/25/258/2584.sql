--Query type: DQL
CREATE TABLE DepartmentCTE
(
    DepartmentNumber INT,
    DepartmentName VARCHAR(50),
    ManagerID INT,
    ParentDepartmentNumber INT,
    SysStartTime DATETIME2,
    SysEndTime DATETIME2
);

INSERT INTO DepartmentCTE
(
    DepartmentNumber,
    DepartmentName,
    ManagerID,
    ParentDepartmentNumber,
    SysStartTime,
    SysEndTime
)
VALUES
(
    1,
    'Sales',
    5,
    0,
    '2013-01-01',
    '2014-01-01'
),
(
    2,
    'Marketing',
    6,
    1,
    '2013-01-01',
    '2014-01-01'
);

WITH DepartmentCTEFiltered AS
(
    SELECT DepartmentNumber, DepartmentName, ManagerID, ParentDepartmentNumber
    FROM DepartmentCTE
    WHERE SysStartTime >= '2013-01-01' AND SysEndTime <= '2014-01-01'
)
SELECT *
FROM DepartmentCTEFiltered
WHERE ManagerID = 5;
-- REMORPH CLEANUP: DROP TABLE DepartmentCTE;