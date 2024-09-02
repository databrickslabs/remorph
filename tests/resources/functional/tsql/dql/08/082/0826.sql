--Query type: DQL
WITH cte AS (SELECT 'admin' AS role_name UNION SELECT 'user' AS role_name) SELECT * FROM cte WHERE IS_MEMBER(role_name) = 1