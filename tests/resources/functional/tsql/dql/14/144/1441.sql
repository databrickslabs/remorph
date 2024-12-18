-- tsql sql:
DECLARE @ANSI_NULLS VARCHAR(3) = 'OFF';
IF ( (16 & @@OPTIONS) = 16 )
    SET @ANSI_NULLS = 'ON';
SELECT value AS Setting
FROM (
    VALUES (@ANSI_NULLS)
) AS T(value);
