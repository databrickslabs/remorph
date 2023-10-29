-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Drop the clustered rowstore index.
DROP INDEX [IDX_CL_MyFactTable]
ON dbo.MyFactTable;
GO
--Create a new clustered columnstore index with the name MyCCI.
CREATE CLUSTERED COLUMNSTORE
INDEX IDX_CCL_MyFactTable ON dbo.MyFactTable;
GO