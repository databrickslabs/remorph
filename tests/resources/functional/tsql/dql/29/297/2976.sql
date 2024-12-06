-- tsql sql:
WITH TempResult AS (
    SELECT 'First Variable' AS var1, 'Second Variable' AS var2
)
SELECT FORMATMESSAGE(20009, var1, var2) AS var1
FROM TempResult;
