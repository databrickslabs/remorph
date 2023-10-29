-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-service-master-key-transact-sql?view=sql-server-ver16

BACKUP SERVICE MASTER KEY TO FILE = 'c:\temp_backups\keys\service_master_key' ENCRYPTION BY PASSWORD = '3dH85Hhk003GHk2597gheij4';