--Query type: DQL
WITH temp_result AS (SELECT 'integer' AS data_type, 'SCALE' AS property_name)
SELECT TYPEPROPERTY(data_type, property_name)
FROM temp_result