-- tsql sql:
DECLARE @ANSI_NULLS_ON VARCHAR(3) = 'OFF';
IF ( (4096 & @@OPTIONS) = 4096 )
    SET @ANSI_NULLS_ON = 'ON';
SELECT value AS ANSI_NULLS_ON
FROM (
    VALUES (@ANSI_NULLS_ON)
) AS temp_result(value);