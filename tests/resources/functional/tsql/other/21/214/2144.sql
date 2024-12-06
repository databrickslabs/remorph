-- tsql sql:
WITH triggers_cte AS (
    SELECT 1 AS object_id, 'abc' AS name
)
SELECT CASE
    WHEN (SELECT TRIGGER_NESTLEVEL((SELECT object_id FROM triggers_cte WHERE name = 'abc'), 'AFTER', 'DDL')) > 5
    THEN 'Trigger abc nested more than 5 levels.'
    ELSE ''
END AS message;
