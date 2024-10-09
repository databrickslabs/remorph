--Query type: TCL
WITH temp_result AS (
    SELECT 1 AS s_suppkey, 'Supplier#000000001' AS s_name, 0.00 AS s_acctbal, '25-989-741-2988' AS s_phone, 'Supplier#000000001 Comment' AS s_comment
    UNION ALL
    SELECT 2 AS s_suppkey, 'Supplier#000000002' AS s_name, 100.00 AS s_acctbal, '25-989-741-2989' AS s_phone, 'Supplier#000000002 Comment' AS s_comment
)
SELECT s_suppkey, s_name, s_acctbal, s_phone, s_comment
FROM temp_result
WHERE s_acctbal > 0.00
ORDER BY s_suppkey DESC;