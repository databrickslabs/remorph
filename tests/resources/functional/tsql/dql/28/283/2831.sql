--Query type: DQL
WITH temp_result AS (
    SELECT 'customer' AS name, 1 AS system_type_id, 2 AS user_type_id, 3 AS schema_id
    UNION ALL
    SELECT 'orders', 4, 5, 6
)
SELECT TYPEPROPERTY(SCHEMA_NAME(schema_id) + '.' + name, 'OwnerId') AS owner_id, name, system_type_id, user_type_id, schema_id
FROM temp_result;