--Query type: DQL
WITH temp_result AS (
    SELECT 'customer' AS table_name, 'c_custkey' AS column_name, 'integer' AS data_type
    UNION ALL
    SELECT 'customer', 'c_name', 'varchar(25)'
    UNION ALL
    SELECT 'customer', 'c_address', 'varchar(40)'
    UNION ALL
    SELECT 'orders', 'o_orderkey', 'integer'
    UNION ALL
    SELECT 'orders', 'o_custkey', 'integer'
    UNION ALL
    SELECT 'orders', 'o_orderstatus', 'char(1)'
)
SELECT *
FROM temp_result;
