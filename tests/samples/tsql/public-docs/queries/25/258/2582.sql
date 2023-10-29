-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/verifysignedbycert-transact-sql?view=sql-server-ver16

SELECT Data, VerifySignedByCert( Cert_Id( 'Shipping04' ),  
    Signed_Data, DataSignature ) AS IsSignatureValid  
FROM [AdventureWorks2022].[SignedData04]   
WHERE Description = N'data signed by certificate ''Shipping04''';  
GO