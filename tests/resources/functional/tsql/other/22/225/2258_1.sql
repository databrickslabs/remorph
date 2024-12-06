-- tsql sql:
CREATE TABLE #BackupInfo
(
    BackupName sysname,
    DatabaseName sysname,
    BackupFile nvarchar(255),
    FileNumber int,
    RecoveryState nvarchar(50)
);

INSERT INTO #BackupInfo
(
    BackupName,
    DatabaseName,
    BackupFile,
    FileNumber,
    RecoveryState
)
VALUES
(
    'MyNewDatabaseBackups',
    'MyNewDatabase',
    'C:\Backups\MyNewDatabase.bak',
    15,
    'NORECOVERY'
);

WITH RestorationProcess AS
(
    SELECT BackupName, DatabaseName, BackupFile, FileNumber, RecoveryState
    FROM #BackupInfo
    WHERE BackupName = 'MyNewDatabaseBackups' AND FileNumber = 15
)
SELECT * FROM RestorationProcess;

DROP TABLE #BackupInfo;
