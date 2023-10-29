-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-object-permissions-transact-sql?view=sql-server-ver16

DENY SELECT ON OBJECT::Person.Address TO RosaQdM;  
GO