-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-schema-transact-sql?view=sql-server-ver16

CREATE SCHEMA Sprockets AUTHORIZATION Krishna   
    CREATE TABLE NineProngs (source INT, cost INT, partnumber INT)  
    GRANT SELECT TO Anibal   
    DENY SELECT TO [Hung-Fu];  
GO