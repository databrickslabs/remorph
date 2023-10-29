-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-application-role-transact-sql?view=sql-server-ver16

CREATE APPLICATION ROLE weekly_receipts   
    WITH PASSWORD = '987G^bv876sPY)Y5m23'   
    , DEFAULT_SCHEMA = Sales;  
GO