-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

ALTER INDEX cci_SimpleTable ON SimpleTable
REBUILD
WITH (DATA_COMPRESSION = COLUMNSTORE);
GO