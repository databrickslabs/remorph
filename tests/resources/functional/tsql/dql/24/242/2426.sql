--Query type: DQL
WITH temp_result AS (SELECT 0xCAFECAFE AS hex_value)
SELECT BASE64_ENCODE(hex_value)
FROM temp_result
