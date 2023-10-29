-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-search-property-list-transact-sql?view=sql-server-ver16

USE database_name;  
GO  
ALTER FULLTEXT INDEX ON table_name START FULL POPULATION;  
GO