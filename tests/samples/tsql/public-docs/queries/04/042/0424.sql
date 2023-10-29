-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Drop all nonclustered indexes
DROP INDEX my_index ON dbo.MyFactTable;