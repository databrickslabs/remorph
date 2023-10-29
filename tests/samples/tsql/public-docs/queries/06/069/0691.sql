-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-sequence-transact-sql?view=sql-server-ver16

ALTER SEQUENCE Test.CountBy1  
    CYCLE  
    CACHE 20 ;