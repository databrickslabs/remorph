-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-resource-pool-transact-sql?view=sql-server-ver16

ALTER RESOURCE POOL "default"  
WITH  
     ( MAX_CPU_PERCENT = 25);  
GO  
ALTER RESOURCE GOVERNOR RECONFIGURE;  
GO