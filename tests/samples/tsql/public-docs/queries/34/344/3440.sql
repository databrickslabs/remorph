-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-master-key-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
RESTORE MASTER KEY   
    FROM FILE = 'c:\backups\keys\AdventureWorks2022_master_key'   
    DECRYPTION BY PASSWORD = '3dH85Hhk003#GHkf02597gheij04'   
    ENCRYPTION BY PASSWORD = '259087M#MyjkFkjhywiyedfgGDFD';  
GO