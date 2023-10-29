-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-index-transact-sql?view=sql-server-ver16

ALTER FULLTEXT INDEX ON table_1
    SET SEARCH PROPERTY LIST OFF WITH NO POPULATION;