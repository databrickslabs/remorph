-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16

ALTER TABLE T1
REBUILD WITH (DATA_COMPRESSION = PAGE) ;