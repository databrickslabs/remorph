-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/db-name-transact-sql?view=sql-server-ver16

SELECT DB_NAME(database_id) AS [Database], database_id  
FROM sys.databases;