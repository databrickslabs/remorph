-- tsql sql:
DECLARE @NewValue INT = 20;
SET @NewValue *= 10;
SELECT @NewValue AS NewValue;
-- REMORPH CLEANUP: DROP VARIABLE @NewValue;
