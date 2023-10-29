-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-xml-schema-collection-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
REVOKE EXECUTE ON XML SCHEMA COLLECTION::Sales.Invoices4 FROM Wanida;  
GO