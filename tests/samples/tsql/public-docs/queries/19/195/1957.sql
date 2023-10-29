-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-type-permissions-transact-sql?view=sql-server-ver16

DENY VIEW DEFINITION ON TYPE::Telemarketing.PhoneNumber   
    TO KhalidR CASCADE;  
GO