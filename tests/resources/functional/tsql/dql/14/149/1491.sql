-- tsql sql:
DECLARE @NOCOUNT VARCHAR(3) = 'OFF';
IF ( (512 & @@OPTIONS) = 512 )
    SET @NOCOUNT = 'ON';
SELECT @NOCOUNT AS NOCOUNT
FROM (
    VALUES (1)
) AS TEMP_TABLE (ID);
