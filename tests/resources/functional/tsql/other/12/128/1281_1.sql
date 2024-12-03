--Query type: DML
DECLARE @VarZ DECIMAL(4, 3) = 0.59;
WITH Studies AS (
  SELECT 0.8 AS Correlation
)
SELECT @VarZ AS VarZ,
       Correlation,
       LEAST(Correlation, 1.0, @VarZ) AS LeastVar
FROM Studies;
-- REMORPH CLEANUP: DROP TABLE Studies;
