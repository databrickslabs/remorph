-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/verifysignedbyasymkey-transact-sql?view=sql-server-ver16

SELECT Data,  
     VerifySignedByAsymKey( AsymKey_Id( 'WillisKey74' ), SignedData,  
     DataSignature ) as IsSignatureValid  
FROM [AdventureWorks2022].[SignedData04]   
WHERE Description = N'data encrypted by asymmetric key ''WillisKey74''';  
GO  
RETURN;