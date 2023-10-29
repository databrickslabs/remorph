-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-resource-pool-transact-sql?view=sql-server-ver16

DROP RESOURCE POOL big_pool;  
GO  
ALTER RESOURCE GOVERNOR RECONFIGURE;  
GO