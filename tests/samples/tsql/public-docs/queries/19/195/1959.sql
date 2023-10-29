-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/enable-trigger-transact-sql?view=sql-server-ver16

DISABLE TRIGGER Person.uAddress ON Person.Address;  
GO  
ENABLE Trigger Person.uAddress ON Person.Address;  
GO