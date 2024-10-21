--Query type: DQL
WITH temp_result AS (SELECT 0xCAFECAFE AS value)
SELECT BASE64_ENCODE(value, 1)
FROM temp_result;