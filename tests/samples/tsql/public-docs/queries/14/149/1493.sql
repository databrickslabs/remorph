-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/else-if-else-transact-sql?view=sql-server-ver16

DECLARE @Number INT;  
SET @Number = 50;  
IF @Number > 100  
   PRINT 'The number is large.';  
ELSE   
   BEGIN  
      IF @Number < 10  
      PRINT 'The number is small.';  
   ELSE  
      PRINT 'The number is medium.';  
   END ;  
GO