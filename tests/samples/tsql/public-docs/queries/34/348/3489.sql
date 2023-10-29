-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-freeproccache-transact-sql?view=sql-server-ver16

USE UserDbSales;
DBCC FREEPROCCACHE (COMPUTE);