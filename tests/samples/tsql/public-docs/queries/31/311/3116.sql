-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-index-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
ALTER FULLTEXT INDEX ON Production.Document
   SET SEARCH PROPERTY LIST DocumentPropertyList;
GO