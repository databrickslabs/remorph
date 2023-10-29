-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-index-transact-sql?view=sql-server-ver16

CREATE FULLTEXT INDEX ON table_1 (column_name) KEY INDEX unique_key_index
    WITH SEARCH PROPERTY LIST=spl_1,
    CHANGE_TRACKING OFF, NO POPULATION;