--Query type: DQL
WITH temp_result AS (
    SELECT n_nationkey AS partition_col, n_regionkey AS order_col, n_nationkey * 10 AS i
    FROM nation
),
lag_result AS (
    SELECT partition_col, order_col, i, LAG(i, 1, 0) OVER (PARTITION BY partition_col ORDER BY order_col) AS NTH_VAL
    FROM temp_result
)
SELECT partition_col, order_col, i, FIRST_VALUE(i) OVER (PARTITION BY partition_col ORDER BY order_col ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS FIRST_VAL, NTH_VAL, LAST_VALUE(i) OVER (PARTITION BY partition_col ORDER BY order_col ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS LAST_VAL
FROM lag_result
ORDER BY partition_col, i, order_col;