--Query type: DDL
WITH TemporaryResult AS (
    SELECT 'DatabaseName' AS DatabaseName, 'RecoveryMode' AS RecoveryMode
)
SELECT *
FROM TemporaryResult;