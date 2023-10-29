-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/databasepropertyex-transact-sql?view=sql-server-ver16

SELECT DATABASEPROPERTYEX(DB_NAME(), 'Updateability');