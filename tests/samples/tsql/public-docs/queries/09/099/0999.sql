-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-resource-pool-transact-sql?view=sql-server-ver16

CREATE EXTERNAL RESOURCE POOL ep_1
WITH (  
    MAX_CPU_PERCENT = 75
    , MAX_MEMORY_PERCENT = 30
);
GO
ALTER RESOURCE GOVERNOR RECONFIGURE;
GO