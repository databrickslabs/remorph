-- tsql sql:
WITH temp_result AS (
    SELECT CAST(SUM(l_extendedprice) AS FLOAT) * SUM(l_discount) AS total_revenue,
           GETDATE() AS [current_date]
    FROM (
        VALUES (1, 10.0, 0.1),
               (2, 20.0, 0.2),
               (3, 30.0, 0.3)
    ) AS lineitem (l_orderkey, l_extendedprice, l_discount)
)
SELECT total_revenue * 100 AS [Total Revenue],
       [current_date] AS [As of]
FROM temp_result;
