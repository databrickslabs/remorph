-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

SELECT *
FROM sys.dm_db_column_store_row_group_physical_stats
WHERE object_id  = object_id('cci_target');