--Query type: DCL
WITH temp_result AS (
    SELECT 'customer' AS type, 'customer_name' AS name, 'customer_address' AS address
    UNION ALL
    SELECT 'supplier' AS type, 'supplier_name' AS name, 'supplier_address' AS address
)
SELECT SUSER_NAME(), USER_NAME()
FROM temp_result;