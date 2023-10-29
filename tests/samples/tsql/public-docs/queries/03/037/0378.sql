-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--1. DROP the existing clustered columnstore index with an automatically-created name, for example:
DROP INDEX ClusteredIndex_1bd8af8797f7453182903cc68df48541 on xdimProduct;
GO
CREATE CLUSTERED COLUMNSTORE INDEX [<new_index_name>]
ON xdimProduct;
GO

--Or,
--2. Change the existing clustered index to a clustered columnstore index with the same name.
CREATE CLUSTERED COLUMNSTORE INDEX [ClusteredIndex_1bd8af8797f7453182903cc68df48541]
ON xdimProduct
WITH ( DROP_EXISTING = ON );
GO