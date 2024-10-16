--Query type: DQL
WITH temp_result AS (SELECT 'customer' AS role_name)
SELECT IS_MEMBER(role_name)
FROM temp_result