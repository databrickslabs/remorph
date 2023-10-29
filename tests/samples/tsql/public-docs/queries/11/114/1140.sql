-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-search-property-list-transact-sql?view=sql-server-ver16

CREATE SEARCH PROPERTY LIST DocumentPropertyList;  
GO  
USE AdventureWorks2022;  
ALTER FULLTEXT INDEX ON Production.Document   
   SET SEARCH PROPERTY LIST DocumentPropertyList  
   WITH NO POPULATION;   
GO