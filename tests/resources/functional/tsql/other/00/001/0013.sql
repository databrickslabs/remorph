--Query type: DDL
CREATE SEQUENCE seq_new;
WITH temp_result AS (
    SELECT 1 AS id, 'value1' AS name
    UNION ALL
    SELECT 2 AS id, 'value2' AS name
)
SELECT id, name
FROM temp_result;
-- REMORPH CLEANUP: DROP SEQUENCE seq_new;