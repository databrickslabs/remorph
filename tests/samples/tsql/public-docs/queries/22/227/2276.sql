-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-type-permissions-transact-sql?view=sql-server-ver16

REVOKE VIEW DEFINITION ON TYPE::Telemarketing.PhoneNumber   
    FROM KhalidR CASCADE;  
GO