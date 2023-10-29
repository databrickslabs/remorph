-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Rebuild the existing clustered columnstore index.
CREATE CLUSTERED COLUMNSTORE INDEX cci_xDimProduct
ON xdimProduct
WITH ( DROP_EXISTING = ON );