-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--For illustration purposes, drop the clustered columnstore index.
--The table continues to be distributed, but changes to a heap.
DROP INDEX cci_xdimProduct ON xDimProduct;
  
--Create a clustered index with a new name, mycci_xDimProduct.
CREATE CLUSTERED COLUMNSTORE INDEX mycci_xDimProduct
ON xdimProduct
WITH ( DROP_EXISTING = OFF );