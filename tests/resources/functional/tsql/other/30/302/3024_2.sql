--Query type: DCL
SET QUOTED_IDENTIFIER ON;

WITH temp_result AS (
    SELECT 1 AS s_suppkey, 'Supplier#000000001' AS s_name, 0.00 AS s_acctbal, '25-989-741-2988' AS s_phone, 'Supplier#000000001 Comment' AS s_comment, 'Nation5' AS n_name, 'Region24' AS r_name
    UNION ALL
    SELECT 2 AS s_suppkey, 'Supplier#000000002' AS s_name, 0.00 AS s_acctbal, '25-989-741-2999' AS s_phone, 'Supplier#000000002 Comment' AS s_comment, 'Nation5' AS n_name, 'Region24' AS r_name
)

SELECT s_suppkey, s_name, SUM(s_acctbal * 0.1) AS total_balance, s_phone, s_comment, n_name, r_name
FROM temp_result
WHERE s_acctbal > 0.00 AND s_suppkey IN (
    SELECT s_suppkey
    FROM temp_result
    GROUP BY s_suppkey
    HAVING SUM(s_acctbal * 0.1) > 1000.00
)
GROUP BY s_suppkey, s_name, s_phone, s_comment, n_name, r_name
ORDER BY total_balance DESC;