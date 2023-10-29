-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-cryptographic-provider-transact-sql?view=sql-server-ver16

ALTER CRYPTOGRAPHIC PROVIDER SecurityProvider  
FROM FILE = 'c:\SecurityProvider\SecurityProvider_v2.dll';  
GO