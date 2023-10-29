-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cot-transact-sql?view=sql-server-ver16

DECLARE @angle FLOAT;  
SET @angle = 124.1332;  
SELECT 'The COT of the angle is: ' + CONVERT(VARCHAR, COT(@angle));  
GO