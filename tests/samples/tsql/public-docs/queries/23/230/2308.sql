-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver16

SELECT 'The number of degrees in PI/2 radians is: ' +   
CONVERT(VARCHAR, DEGREES((PI()/2)));  
GO