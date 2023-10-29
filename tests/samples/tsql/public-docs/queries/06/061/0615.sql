-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

ALTER INDEX test_idx on test_table RESUME WITH (MAXDOP = 4) ;