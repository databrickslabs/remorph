-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-broker-priority-transact-sql?view=sql-server-ver16

ALTER BROKER PRIORITY SimpleContractDefaultPriority  
    FOR CONVERSATION  
    SET (PRIORITY_LEVEL = 3);