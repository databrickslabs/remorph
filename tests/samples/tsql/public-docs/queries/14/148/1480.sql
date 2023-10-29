-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/unary-operators-positive?view=sql-server-ver16

DECLARE @MyNumber DECIMAL(10,2);  
SET @MyNumber = +123.45;  
SELECT @MyNumber;  
GO