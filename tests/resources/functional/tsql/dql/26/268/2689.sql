--Query type: DQL
WITH OrdersCTE AS (
    SELECT 'O' + CONVERT(VARCHAR, ROW_NUMBER() OVER (ORDER BY c_custkey)) AS O_OrderKey,
           'OS' + CONVERT(VARCHAR, c_nationkey) AS O_OrderStatus
    FROM (
        VALUES (1, 1),
               (2, 2),
               (3, 3)
    ) AS customer(c_custkey, c_nationkey)
)
SELECT O_OrderStatus,
       COUNT(DISTINCT O_OrderKey) AS Approx_Distinct_OrderKey
FROM OrdersCTE
GROUP BY O_OrderStatus
ORDER BY O_OrderStatus;