-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/sin-transact-sql?view=sql-server-ver16

DECLARE @angle FLOAT;  
SET @angle = 45.175643;  
SELECT 'The SIN of the angle is: ' + CONVERT(VARCHAR, SIN(@angle));  
GO