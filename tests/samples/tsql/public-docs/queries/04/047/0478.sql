-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-asymmetric-key-transact-sql?view=sql-server-ver16

ALTER ASYMMETRIC KEY PacificSales09   
    WITH PRIVATE KEY (  
    DECRYPTION BY PASSWORD = '<oldPassword>',  
    ENCRYPTION BY PASSWORD = '<enterStrongPasswordHere>');  
GO