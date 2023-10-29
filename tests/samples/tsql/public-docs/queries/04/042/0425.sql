-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Drop the clustered columnstore index and create a clustered rowstore index.
--All of the columns are stored in the rowstore clustered index.
--The columns listed are the included columns in the index.
CREATE CLUSTERED INDEX cci_xDimProduct
ON xdimProduct (ProductKey, ProductAlternateKey, ProductSubcategoryKey, WeightUnitMeasureCode)
WITH ( DROP_EXISTING = ON);