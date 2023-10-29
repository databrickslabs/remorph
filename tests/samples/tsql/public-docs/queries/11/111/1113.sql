-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-resource-pool-transact-sql?view=sql-server-ver16

CREATE RESOURCE POOL bigPool;  
GO  
ALTER RESOURCE GOVERNOR RECONFIGURE;  
GO