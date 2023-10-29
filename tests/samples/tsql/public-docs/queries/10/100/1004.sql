-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE EXTERNAL TABLE vw_sys_servers_ro
(    name sysname NOT NULL )
WITH (DATA_SOURCE = [DataSource_SQLInstanceListener_ReadOnlyIntent], LOCATION = N'dbname.dbo.vw_sys_servers');
GO
CREATE EXTERNAL TABLE vw_sys_servers_rw
(    name sysname NOT NULL)
WITH (DATA_SOURCE = [DataSource_SQLInstanceListener_ReadWriteIntent], LOCATION = N'dbname.dbo.vw_sys_servers');
GO
SELECT [name] FROM dbo.vw_sys_servers_ro; --should return secondary replica instance
SELECT [name] FROM dbo.vw_sys_servers_rw; --should return primary replica instance
GO