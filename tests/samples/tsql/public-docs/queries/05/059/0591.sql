-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

ALTER INDEX IX_INDEX1
ON T1
REBUILD
WITH (DATA_COMPRESSION = PAGE);
GO