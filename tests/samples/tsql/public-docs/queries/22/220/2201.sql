-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/encryptbycert-transact-sql?view=sql-server-ver16

INSERT INTO [AdventureWorks2022].[ProtectedData04]   
    VALUES ( N'Data encrypted by certificate ''Shipping04''',  
    EncryptByCert(Cert_ID('JanainaCert02'), @cleartext) );  
GO