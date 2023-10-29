-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Rebuild the entire index by using ALTER INDEX and the REBUILD option.
ALTER INDEX IDX_CL_MyFactTable
ON dbo.[MyFactTable]
REORGANIZE;