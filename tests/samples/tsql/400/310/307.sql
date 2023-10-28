UPDATE Archive.dbo.Records  
SET [Chart] = CAST('Xray 1' as VARBINARY(max))  
WHERE [SerialNumber] = 2;