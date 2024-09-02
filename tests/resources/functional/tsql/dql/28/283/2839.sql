--Query type: DQL
WITH temp_result AS (
    SELECT 'customer' AS table_name, c_custkey AS key_value
    FROM customer
    UNION ALL
    SELECT 'orders' AS table_name, o_orderkey AS key_value
    FROM orders
    UNION ALL
    SELECT 'lineitem' AS table_name, l_orderkey AS key_value
    FROM lineitem
)
SELECT SUSER_NAME() AS user_name, table_name, key_value
FROM temp_result;