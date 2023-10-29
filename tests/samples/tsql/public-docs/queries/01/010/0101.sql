-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-cryptographic-provider-transact-sql?view=sql-server-ver16

-- Install the provider  
CREATE CRYPTOGRAPHIC PROVIDER SecurityProvider  
    FROM FILE = 'C:\SecurityProvider\SecurityProvider_v1.dll';