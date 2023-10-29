-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql?view=sql-server-ver16

ALTER DATABASE CustomerSales
    SET ( DISTRIBUTED_SIZE = 1000 GB );