--Query type: TCL
DECLARE @sql NVARCHAR(MAX) = N'RESTORE LOG MyNewDatabase FROM (VALUES (1, ''BackupFile1''), (2, ''BackupFile2'')) AS BackupFiles(FileNumber, FileName) WITH FILE = 1, NORECOVERY;';
EXEC sp_executesql @sql;
SELECT *
FROM (VALUES (1, 'BackupFile1'), (2, 'BackupFile2')) AS BackupFiles(FileNumber, FileName);