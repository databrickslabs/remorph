--Query type: DML
DECLARE @VarZ DECIMAL(4, 3) = 0.71;
SELECT @VarZ AS VarZ, Correlation, IIF(Correlation > @VarZ, Correlation, @VarZ) AS GreatestVar
FROM (VALUES (0.2), (0.9), (0.1)) AS Studies(Correlation);
-- REMORPH CLEANUP: DROP TABLE Studies;
-- REMORPH CLEANUP: DEALLOCATE @VarZ;
