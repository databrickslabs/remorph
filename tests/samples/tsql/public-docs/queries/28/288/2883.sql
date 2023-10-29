-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-database-mirroring?view=sql-server-ver16

SELECT db.name, m.mirroring_role_desc
FROM sys.database_mirroring m
JOIN sys.databases db
ON db.database_id = m.database_id
WHERE db.name = N'AdventureWorks2022';
GO