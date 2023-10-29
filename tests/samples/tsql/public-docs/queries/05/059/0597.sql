-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

ALTER INDEX cci_FactInternetSales2 ON FactInternetSales2 REBUILD;
SELECT * FROM sys.column_store_row_groups;