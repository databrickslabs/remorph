-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-synonym-transact-sql?view=sql-server-ver16

USE tempdb;  
GO  
-- Create a synonym for the Product table in AdventureWorks2022.  
CREATE SYNONYM MyProduct  
FOR AdventureWorks2022.Production.Product;  
GO  
-- Drop synonym MyProduct.  
USE tempdb;  
GO  
DROP SYNONYM MyProduct;  
GO