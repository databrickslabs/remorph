-- tsql sql:
WITH temp_result AS (
    SELECT CAST(0.5 AS DECIMAL(2, 1)) AS VarY, CAST(0.3 AS DECIMAL(3, 1)) AS Correlation
    UNION ALL
    SELECT CAST(0.2 AS DECIMAL(2, 1)), CAST(0.1 AS DECIMAL(3, 1))
)
SELECT VarY, Correlation
FROM temp_result
WHERE Correlation > (
    SELECT GREATEST(Correlation, Correlation)
    FROM (
        VALUES (CAST(0.7 AS DECIMAL(2, 1))), (CAST(0.65 AS DECIMAL(3, 1)))
    ) AS temp(Correlation)
);
