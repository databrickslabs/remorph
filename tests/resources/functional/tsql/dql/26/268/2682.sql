-- tsql sql:
DECLARE @NextValue INT;
SET @NextValue = NEXT VALUE FOR IncrementingSeq;
WITH TempResult AS (
    SELECT @NextValue AS Value
)
SELECT *
FROM TempResult;
-- REMORPH CLEANUP: DROP SEQUENCE IncrementingSeq;
