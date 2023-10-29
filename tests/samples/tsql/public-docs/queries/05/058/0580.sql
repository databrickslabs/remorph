-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-external-resource-pool-transact-sql?view=sql-server-ver16

ALTER EXTERNAL RESOURCE POOL ep_1
WITH (
    MAX_CPU_PERCENT = 50
    , MAX_MEMORY_PERCENT = 25
);
GO
ALTER RESOURCE GOVERNOR RECONFIGURE;
GO