-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-symmetric-key-transact-sql?view=sql-server-ver16

BACKUP SYMMETRIC KEY symmetric_key 
   TO URL = 'https://mydocsteststorage.blob.core.windows.net/mytestcontainer/symmetric_key.bak'
   ENCRYPTION BY PASSWORD = '3dH85Hhk003GHk2597gheij4'