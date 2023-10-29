-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-broker-priority-transact-sql?view=sql-server-ver16

CREATE BROKER PRIORITY SimpleContractDefaultPriority  
    FOR CONVERSATION  
    SET (CONTRACT_NAME = SimpleContract,  
         LOCAL_SERVICE_NAME = ANY,  
         REMOTE_SERVICE_NAME = ANY,  
         PRIORITY_LEVEL = 7);