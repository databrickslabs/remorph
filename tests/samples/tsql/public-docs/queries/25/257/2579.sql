-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/verifysignedbyasymkey-transact-sql?view=sql-server-ver16

SELECT Data   
FROM [AdventureWorks2022].[SignedData04]   
WHERE VerifySignedByAsymKey( AsymKey_Id( 'WillisKey74' ), Data,  
     DataSignature ) = 1  
AND Description = N'data encrypted by asymmetric key ''WillisKey74''';  
GO