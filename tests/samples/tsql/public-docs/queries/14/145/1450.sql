-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-cursor-close-on-commit-transact-sql?view=sql-server-ver16

DECLARE @CURSOR_CLOSE VARCHAR(3) = 'OFF';  
IF ( (4 & @@OPTIONS) = 4 ) SET @CURSOR_CLOSE = 'ON';  
SELECT @CURSOR_CLOSE AS CURSOR_CLOSE_ON_COMMIT;