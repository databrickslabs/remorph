-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-file-and-filegroup-options?view=sql-server-ver16

USE master;
GO
ALTER DATABASE AdventureWorks2022
MODIFY FILEGROUP Test1FG1 DEFAULT;
GO
ALTER DATABASE AdventureWorks2022
MODIFY FILEGROUP [PRIMARY] DEFAULT;
GO