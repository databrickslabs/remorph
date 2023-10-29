-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-concatenation-equal-transact-sql?view=sql-server-ver16

DECLARE @v1 VARCHAR(40);  
SET @v1 = 'This is the original.';  
SET @v1 += ' More text.';  
PRINT @v1;