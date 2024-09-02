--Query type: DDL
CREATE TABLE #EmployeePhoto
(
    EmployeeId INT NOT NULL PRIMARY KEY,
    Photo VARBINARY(MAX) NULL,
    MyRowGuidColumn UNIQUEIDENTIFIER NOT NULL UNIQUE DEFAULT NEWID()
);

INSERT INTO #EmployeePhoto (EmployeeId, Photo)
VALUES (1, CONVERT(VARBINARY(MAX), 'Some photo data'));

SELECT * FROM #EmployeePhoto;

-- REMORPH CLEANUP: DROP TABLE #EmployeePhoto;