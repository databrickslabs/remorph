-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

RESTORE DATABASE AdventureWorks2022
    FROM DISK = 'Z:\SQLServerBackups\AdventureWorks2022.bak'
    WITH FILE = 6,
      NORECOVERY;
RESTORE DATABASE AdventureWorks2022
    FROM DISK = 'Z:\SQLServerBackups\AdventureWorks2022.bak'
    WITH FILE = 9,
      RECOVERY;