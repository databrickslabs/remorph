--Query type: DML
DECLARE @a DECIMAL(10,3) = 75.123, @b FLOAT(53) = 75.123;
WITH cte AS (
    SELECT @a * @b AS product
)
SELECT ISNULL(CAST(product AS DECIMAL(10,3)), 0) AS result
FROM cte;

SELECT *
FROM (
    VALUES (ISNULL(CAST(@a * @b AS DECIMAL(10,3)), 0))
) AS cte(result);
-- REMORPH CLEANUP: None;