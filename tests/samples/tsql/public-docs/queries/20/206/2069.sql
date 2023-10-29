-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/serverproperty-transact-sql?view=sql-server-ver16

EXEC sp_dropserver 'current_server_name';
GO
EXEC sp_addserver 'new_server_name', 'local';
GO