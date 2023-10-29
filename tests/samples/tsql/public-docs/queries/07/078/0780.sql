-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql?view=sql-server-ver16

BACKUP DATABASE AdventureWorks2022
TO DISK = 'X:\SQLServerBackups\AdventureWorks1.bak',
DISK = 'Y:\SQLServerBackups\AdventureWorks2.bak',
DISK = 'Z:\SQLServerBackups\AdventureWorks3.bak'
WITH FORMAT,
  MEDIANAME = 'AdventureWorksStripedSet0',
  MEDIADESCRIPTION = 'Striped media set for AdventureWorks2022 database';
GO