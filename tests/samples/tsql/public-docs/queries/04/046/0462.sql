-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-cryptographic-provider-transact-sql?view=sql-server-ver16

/* First, disable provider to perform the upgrade.  
This will terminate all open cryptographic sessions. */  
ALTER CRYPTOGRAPHIC PROVIDER SecurityProvider   
SET ENABLED = OFF;  
GO  
/* Drop the provider. */  
DROP CRYPTOGRAPHIC PROVIDER SecurityProvider;  
GO