-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkident-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
DBCC CHECKIDENT ('Person.AddressType', RESEED, 10);
GO