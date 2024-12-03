--Query type: DML
DECLARE @myNewVariable DECIMAL(5, 2);
SET @myNewVariable = 25.5;
SET @myNewVariable /= 3;
WITH tempResult AS (
    SELECT @myNewVariable AS NewResultVariable
)
SELECT *
FROM tempResult;
