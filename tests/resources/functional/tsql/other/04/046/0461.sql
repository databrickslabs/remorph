--Query type: DML
DECLARE @NewBalance INT;
SET @NewBalance = 10;
SET @NewBalance = @NewBalance * 10;
WITH temp_table AS (
    SELECT 1 AS temp_column
)
SELECT TOP 1 @NewBalance AS NewBalance
FROM temp_table;
