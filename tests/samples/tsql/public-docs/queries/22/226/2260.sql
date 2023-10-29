-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

RESTORE DATABASE Sales
  FROM DISK = 'D:\MSSQL\Backup\SalesSnapshotFull.bkm'
  WITH METADATA_ONLY,
  NORECOVERY;

RESTORE LOG Sales
  FROM DISK = 'D:\MSSQL\Backup\SalesLog.trn'
  WITH RECOVERY;