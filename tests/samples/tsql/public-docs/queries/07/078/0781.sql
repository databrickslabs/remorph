-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql?view=sql-server-ver16

BACKUP DATABASE AdventureWorks2022
TO DISK = 'X:\SQLServerBackups\AdventureWorks1a.bak',
  DISK = 'Y:\SQLServerBackups\AdventureWorks2a.bak',
  DISK = 'Z:\SQLServerBackups\AdventureWorks3a.bak'
MIRROR TO DISK='X:\SQLServerBackups\AdventureWorks1b.bak',
  DISK = 'Y:\SQLServerBackups\AdventureWorks2b.bak',
  DISK = 'Z:\SQLServerBackups\AdventureWorks3b.bak';
GO