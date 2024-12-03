--Query type: DML
DECLARE @g geography = 'LINESTRING(1 2, 5 6)';
WITH temp_result AS (
  SELECT @g.BufferWithCurves(1.0) AS buffered
)
SELECT buffered.ToString() AS result
FROM temp_result;
-- REMORPH CLEANUP: DROP TABLE temp_result;
