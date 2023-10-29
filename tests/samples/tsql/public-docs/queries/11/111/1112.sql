-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-resource-pool-transact-sql?view=sql-server-ver16

CREATE RESOURCE POOL PoolAdmin  
WITH (  
    MIN_IOPS_PER_VOLUME = 20,  
    MAX_IOPS_PER_VOLUME = 100  
      );