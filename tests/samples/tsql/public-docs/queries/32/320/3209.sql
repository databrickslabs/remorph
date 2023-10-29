-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-xml-schema-collection-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
DENY EXECUTE ON XML SCHEMA COLLECTION::Sales.Invoices4 TO Wanida;  
GO