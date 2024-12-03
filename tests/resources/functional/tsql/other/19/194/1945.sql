--Query type: DML
CREATE TABLE #MyTempTable
(
    Name VARCHAR(50),
    GroupName VARCHAR(50),
    DepartmentID INT
);

INSERT INTO #MyTempTable (Name, GroupName, DepartmentID)
VALUES
    ('Department1', 'Group1', 18),
    ('Department2', 'Group2', 19),
    ('Department3', 'Group3', 20);

DELETE FROM #MyTempTable
WHERE DepartmentID = 18;

SELECT *
FROM #MyTempTable;

-- REMORPH CLEANUP: DROP TABLE #MyTempTable;
