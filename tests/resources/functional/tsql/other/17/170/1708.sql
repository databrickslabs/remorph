--Query type: DML
DECLARE @g geometry = 'LINESTRING(3 4, 8 9, 5 6)';
WITH temp AS (
  SELECT @g AS geom
)
SELECT
  CASE
    WHEN geom.MinDbCompatibilityLevel() <= 100 THEN geom.ToString()
    ELSE NULL
  END AS result
FROM temp;
