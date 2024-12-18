-- tsql sql:
DECLARE @ANSI_NULLS VARCHAR(3) = 'OFF';
IF ( (1 & @@OPTIONS) = 1 )
    SET @ANSI_NULLS = 'ON';
SELECT *
FROM (
    VALUES (@ANSI_NULLS)
) AS temp_result(ANSI_NULLS);
