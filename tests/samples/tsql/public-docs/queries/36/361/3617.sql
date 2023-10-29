-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/unary-operators-negative?view=sql-server-ver16

USE tempdb;  
GO  
DECLARE @MyNumber DECIMAL(10,2);  
SET @MyNumber = -123.45;  
SELECT @MyNumber AS NegativeValue;  
GO