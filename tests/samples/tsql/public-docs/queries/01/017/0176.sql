-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
IF EXISTS (SELECT name FROM sys.tables
    WHERE name = N'xDimProduct'
    AND object_id = OBJECT_ID (N'xDimProduct'))
DROP TABLE xDimProduct;
  
--Create a distributed table with a clustered index.
CREATE TABLE xDimProduct (ProductKey, ProductAlternateKey, ProductSubcategoryKey)
WITH ( DISTRIBUTION = HASH(ProductKey),
    CLUSTERED INDEX (ProductKey) )
AS SELECT ProductKey, ProductAlternateKey, ProductSubcategoryKey FROM DimProduct;