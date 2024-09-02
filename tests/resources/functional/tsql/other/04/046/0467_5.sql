--Query type: DCL
DECLARE @total DECIMAL;
SET @total = 100.00;
WITH temp AS (
    SELECT @total AS TotalAmount
)
SELECT * FROM temp;