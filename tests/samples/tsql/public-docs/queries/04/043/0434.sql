-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/checksum-agg-transact-sql?view=sql-server-ver16

--Get the checksum value before the column value is changed.  

SELECT CHECKSUM_AGG(CAST(Quantity AS INT))  
FROM Production.ProductInventory;  
GO