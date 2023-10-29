-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql?view=sql-server-ver16

ALTER DATABASE CustomerSales
    SET ( REPLICATED_SIZE = 1 GB );