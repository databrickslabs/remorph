-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/setuser-transact-sql?view=sql-server-ver16

SETUSER 'mary';  
GO  
GRANT SELECT ON computer_types TO joe;  
GO  
--To revert to the original user  
SETUSER;