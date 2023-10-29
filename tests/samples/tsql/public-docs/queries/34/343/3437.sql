-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-master-key-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'sfj5300osdVdgwdfkli7';  
BACKUP MASTER KEY TO FILE = 'c:\temp\AdventureWorks2022_master_key'   
    ENCRYPTION BY PASSWORD = 'sd092735kjn$&adsg';  
GO