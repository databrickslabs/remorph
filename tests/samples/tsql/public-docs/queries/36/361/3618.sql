-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/unary-operators-positive?view=sql-server-ver16

USE tempdb;  
GO  
DECLARE @Num1 INT;  
SET @Num1 = -5;  
SELECT +@Num1, ABS(@Num1);  
GO