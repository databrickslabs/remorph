-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-catalog-transact-sql?view=sql-server-ver16

--Change to accent insensitive  
USE AdventureWorks2022;  
GO  
ALTER FULLTEXT CATALOG ftCatalog   
REBUILD WITH ACCENT_SENSITIVITY=OFF;  
GO  
-- Check Accentsensitivity  
SELECT FULLTEXTCATALOGPROPERTY('ftCatalog', 'accentsensitivity');  
GO  
--Returned 0, which means the catalog is not accent sensitive.