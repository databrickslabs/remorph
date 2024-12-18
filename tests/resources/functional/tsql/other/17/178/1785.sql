-- tsql sql:
DECLARE @g geometry = 'LINESTRING(1 2, 5 6);
WITH temp_result AS (
    SELECT @g AS geom
)
SELECT geom.BufferWithCurves(3).ToString()
FROM temp_result;
-- REMORPH CLEANUP: DROP VARIABLE @g;
