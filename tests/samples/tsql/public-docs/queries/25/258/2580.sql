-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/verifysignedbycert-transact-sql?view=sql-server-ver16

SELECT Data FROM [AdventureWorks2022].[SignedData04]   
WHERE VerifySignedByCert( Cert_Id( 'Shipping04' ), Data,   
    DataSignature ) = 1   
AND Description = N'data signed by certificate ''Shipping04''';  
GO