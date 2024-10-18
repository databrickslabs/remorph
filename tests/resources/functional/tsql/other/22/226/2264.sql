--Query type: DCL
CREATE TABLE RestoreLog
(
    LogID INT IDENTITY(1, 1) PRIMARY KEY,
    DatabaseName VARCHAR(255),
    FileName VARCHAR(255),
    OldLocation VARCHAR(255),
    NewLocation VARCHAR(255),
    RestoreDate DATETIME DEFAULT GETDATE()
);

WITH DatabaseFiles AS
(
    SELECT 'Marketing_Data1' AS FileName, 'https://mystorageaccount.blob.core.windows.net/mythirdcontainer/Marketing_Data1.mdf' AS OldLocation, 'https://mystorageaccount.blob.core.windows.net/mysecondcontainer/Marketing_Data1.mdf' AS NewLocation
    UNION ALL
    SELECT 'Marketing_log', 'https://mystorageaccount.blob.core.windows.net/mythirdcontainer/Marketing_log.ldf', 'https://mystorageaccount.blob.core.windows.net/mysecondcontainer/Marketing_log.ldf'
)
INSERT INTO RestoreLog (DatabaseName, FileName, OldLocation, NewLocation)
SELECT 'Marketing', FileName, OldLocation, NewLocation
FROM DatabaseFiles;

SELECT * FROM RestoreLog;
-- REMORPH CLEANUP: DROP TABLE RestoreLog;