-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

ALTER INDEX index1 ON table1 REBUILD;

ALTER INDEX ALL ON table1 REBUILD;

ALTER INDEX ALL ON dbo.table1 REBUILD;