-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-symmetric-key-transact-sql?view=sql-server-ver16

RESTORE SYMMETRIC KEY symmetric_key 
   FROM URL = 'https://mydocsteststorage.blob.core.windows.net/mytestcontainer/symmetric_key.bak'
   DECRYPTION BY PASSWORD = '3dH85Hhk003#GHkf02597gheij04'   
   ENCRYPTION BY PASSWORD = '259087M#MyjkFkjhywiyedfgGDFD';