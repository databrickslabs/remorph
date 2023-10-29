-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-file-and-filegroup-options?view=sql-server-ver16

USE master;
GO

ALTER DATABASE AdventureWorks2022
MODIFY FILE
(NAME = test1dat3,
SIZE = 200MB);
GO