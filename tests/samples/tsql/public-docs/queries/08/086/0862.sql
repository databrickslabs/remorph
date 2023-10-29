-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-asymmetric-key-transact-sql?view=sql-server-ver16

CREATE ASYMMETRIC KEY PacificSales09   
    WITH ALGORITHM = RSA_2048   
    ENCRYPTION BY PASSWORD = '<enterStrongPasswordHere>';   
GO