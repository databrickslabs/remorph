-- tsql sql:
DECLARE @password nvarchar(50) = 'backup_password';
DECLARE @url nvarchar(200) = 'https://mynewdocsteststorage.blob.core.windows.net/mynewtestcontainer/MyNewDB_master_key.bak';
DECLARE @sql nvarchar(max);

OPEN MASTER KEY DECRYPTION BY PASSWORD = 'mynewpassword';

SET @sql = 'BACKUP MASTER KEY TO FILE = ''' + @url + ''' ENCRYPTION BY PASSWORD = ''' + @password + '''';
EXEC sp_executesql @sql;

-- To verify the master key backup, you can use the following query:
SELECT * FROM sys.symmetric_keys;
-- This will show you the symmetric keys in the database, including the master key.

-- REMORPH CLEANUP: No objects were created in this query, so no cleanup is necessary.
