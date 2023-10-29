-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-asymmetric-key-transact-sql?view=sql-server-ver16

OPEN MASTER KEY DECRYPTION BY PASSWORD = '<database master key password>';  
ALTER ASYMMETRIC KEY PacificSales09 WITH PRIVATE KEY (  
    DECRYPTION BY PASSWORD = '<enterStrongPasswordHere>' );  
GO