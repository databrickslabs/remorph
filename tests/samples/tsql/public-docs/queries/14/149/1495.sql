-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-quoted-identifier-transact-sql?view=sql-server-ver16

DECLARE @QUOTED_IDENTIFIER VARCHAR(3) = 'OFF';
IF ( (256 & @@OPTIONS) = 256 ) 
BEGIN
    SET @QUOTED_IDENTIFIER = 'ON';
END

SELECT @QUOTED_IDENTIFIER AS QUOTED_IDENTIFIER;