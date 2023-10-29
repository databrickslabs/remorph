-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Drop the clustered columnstore index. The table continues to be distributed, but changes to a heap.
DROP INDEX cci_xdimProduct ON xdimProduct;