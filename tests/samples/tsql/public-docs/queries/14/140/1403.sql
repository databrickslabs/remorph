-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-indexdefrag-transact-sql?view=sql-server-ver16

DBCC INDEXDEFRAG (AdventureWorks2022, 'Production.Product', PK_Product_ProductID);
GO