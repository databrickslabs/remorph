-- tsql sql:
DECLARE @y1 INT = 30;
SET @y1 += 3;
WITH temp_result AS (
    SELECT @y1 AS Added_3
)
SELECT *
FROM temp_result;
-- REMORPH CLEANUP: DROP TABLE temp_result;
