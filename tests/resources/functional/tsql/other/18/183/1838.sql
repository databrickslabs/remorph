--Query type: DML
WITH numbers AS (
    SELECT CAST(1.00 AS DECIMAL(10, 2)) AS myvalue
    UNION ALL
    SELECT CAST(myvalue + 1.00 AS DECIMAL(10, 2))
    FROM numbers
    WHERE myvalue < 10.00
)
SELECT SQRT(CAST(myvalue AS float)) AS sqrt_myvalue
FROM numbers
OPTION (MAXRECURSION 0);