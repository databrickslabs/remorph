-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-external-resource-pool-transact-sql?view=sql-server-ver16

DROP EXTERNAL RESOURCE POOL ex_pool;  
GO  
ALTER RESOURCE GOVERNOR RECONFIGURE;  
GO