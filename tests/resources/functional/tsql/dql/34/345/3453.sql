-- tsql sql:
WITH temp_result AS (SELECT 'Harold' AS username)
SELECT USER_ID(username)
FROM temp_result;
