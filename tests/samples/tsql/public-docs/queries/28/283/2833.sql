-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/type-id-transact-sql?view=sql-server-ver16

SELECT TYPE_NAME(TYPE_ID('datetime')) AS [TYPE_NAME]  
    ,TYPE_ID('datetime') AS [TYPE_ID];  
GO