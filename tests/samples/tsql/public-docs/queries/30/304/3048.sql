-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/checksum-agg-transact-sql?view=sql-server-ver16

UPDATE Production.ProductInventory   
SET Quantity=125  
WHERE Quantity=100;  
GO  

--Get the checksum of the modified column.  
SELECT CHECKSUM_AGG(CAST(Quantity AS INT))  
FROM Production.ProductInventory;