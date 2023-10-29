-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/encryptbyasymkey-transact-sql?view=sql-server-ver16

INSERT INTO AdventureWorks2022.Sales.ProtectedData04   
    VALUES( N'Data encrypted by asymmetric key ''JanainaAsymKey02''',  
    EncryptByAsymKey(AsymKey_ID('JanainaAsymKey02'), @cleartext) );  
GO