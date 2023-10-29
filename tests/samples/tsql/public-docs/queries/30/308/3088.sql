-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

DELETE TOP(1) dbo.DatabaseLog WITH (READPAST)
OUTPUT DELETED.*
WHERE DatabaseLogID = 7;
GO