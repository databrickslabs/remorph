-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/open-symmetric-key-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
OPEN SYMMETRIC KEY SymKeyMarketing3   
    DECRYPTION BY CERTIFICATE MarketingCert9;  
GO