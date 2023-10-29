-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

DROP INDEX dbo.SimpleTable.nc1_simple;
DROP INDEX dbo.SimpleTable.nc2_simple;
  
--Convert the rowstore table to a columnstore index.
CREATE CLUSTERED COLUMNSTORE INDEX cci_simple ON dbo.SimpleTable;
GO