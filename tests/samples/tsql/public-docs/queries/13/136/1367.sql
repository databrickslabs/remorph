-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE VIEW vw_sys_servers AS
SELECT [name] FROM sys.servers
WHERE server_id = 0;
GO