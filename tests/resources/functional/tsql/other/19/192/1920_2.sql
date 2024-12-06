-- tsql sql:
DECLARE @y4 INT = 30;
SET @y4 *= 3;
SELECT @y4 AS Multiplied_by_3
FROM (
    VALUES (1)
) AS dummy_table(dummy_column);
-- REMORPH CLEANUP: DROP VARIABLE @y4;
