-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

ALTER INDEX cci_fact3
ON fact3
REBUILD PARTITION = 12;