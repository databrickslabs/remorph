-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-service-master-key-transact-sql?view=sql-server-ver16

RESTORE SERVICE MASTER KEY   
    FROM FILE = 'c:\temp_backups\keys\service_master_key'   
    DECRYPTION BY PASSWORD = '3dH85Hhk003GHk2597gheij4';  
GO