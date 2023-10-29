-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

USE master;
RESTORE DATABASE AdventureWorks2022 FROM DATABASE_SNAPSHOT = 'AdventureWorks_dbss1800';
GO