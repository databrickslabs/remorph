-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-certificate-transact-sql?view=sql-server-ver16

ALTER CERTIFICATE Shipping11   
    WITH PRIVATE KEY (DECRYPTION BY PASSWORD = '95hkjdskghFDGGG4%',  
    ENCRYPTION BY PASSWORD = '34958tosdgfkh##38');  
GO