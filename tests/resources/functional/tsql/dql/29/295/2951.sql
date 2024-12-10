-- tsql sql:
WITH temp_result AS (
    SELECT request_id, session_id
    FROM (
        VALUES (1, 1), (2, 2), (3, 3)
    ) AS requests (request_id, session_id)
)
SELECT request_id
FROM temp_result
WHERE session_id = (SELECT @@spid);
