-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/unary-operators-negative?view=sql-server-ver16

USE tempdb;  
GO  
DECLARE @Num1 INT;  
SET @Num1 = 5;  
SELECT @Num1 AS VariableValue, -@Num1 AS NegativeValue;  
GO