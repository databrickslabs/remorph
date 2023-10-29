-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-application-role-transact-sql?view=sql-server-ver16

ALTER APPLICATION ROLE receipts_ledger   
    WITH NAME = weekly_ledger,   
    PASSWORD = '897yUUbv77bsrEE00nk2i',   
    DEFAULT_SCHEMA = Production;  
GO