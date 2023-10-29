-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-arithignore-transact-sql?view=sql-server-ver16

DECLARE @ARITHIGNORE VARCHAR(3) = 'OFF';  
IF ( (128 & @@OPTIONS) = 128 ) SET @ARITHIGNORE = 'ON';  
SELECT @ARITHIGNORE AS ARITHIGNORE;