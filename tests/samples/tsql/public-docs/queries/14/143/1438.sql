-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-ansi-null-dflt-off-transact-sql?view=sql-server-ver16

DECLARE @ANSI_NULL_DFLT_OFF VARCHAR(3) = 'OFF';  
IF ( (2048 & @@OPTIONS) = 2048 ) SET @ANSI_NULL_DFLT_OFF = 'ON';  
SELECT @ANSI_NULL_DFLT_OFF AS ANSI_NULL_DFLT_OFF;