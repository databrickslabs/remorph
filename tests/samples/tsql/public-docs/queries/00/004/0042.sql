-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/signbyasymkey-transact-sql?view=sql-server-ver16

-- Create a table in which to store the data  
CREATE TABLE [SignedData04](Description NVARCHAR(max), Data NVARCHAR(max), DataSignature VARBINARY(8000));  
GO  
-- Store data together with its signature  
DECLARE @clear_text_data NVARCHAR(max);  
set @clear_text_data = N'Important numbers 2, 3, 5, 7, 11, 13, 17,   
      19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,  
      83, 89, 97';  
INSERT INTO [SignedData04]   
    VALUES( N'data encrypted by asymmetric key ''PrimeKey''',  
    @clear_text_data, SignByAsymKey( AsymKey_Id( 'PrimeKey' ),  
    @clear_text_data, N'pGFD4bb925DGvbd2439587y' ));  
GO