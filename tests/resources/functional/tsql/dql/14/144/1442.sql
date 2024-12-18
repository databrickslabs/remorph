-- tsql sql:
DECLARE @ANSI_NULLS VARCHAR(3) = 'OFF';
IF ( (1 & @@OPTIONS) = 1 )
    SET @ANSI_NULLS = 'ON';

WITH TempResult AS (
    SELECT 1 AS OptionValue
)
SELECT @ANSI_NULLS AS ANSI_NULLS, OptionValue
FROM TempResult;
