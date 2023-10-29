-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

INSERT INTO cci_target WITH (TABLOCK)
SELECT TOP 300000 * FROM staging;