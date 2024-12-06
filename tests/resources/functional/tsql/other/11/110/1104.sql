-- tsql sql:
WITH temp_sql_log AS (
    SELECT * FROM (VALUES ('log1'), ('log2')) AS log(log)
),
 temp_service_queues AS (
    SELECT * FROM (VALUES ('queue1'), ('queue2')) AS queue(queue)
)
SELECT 'SQL Log' AS Source, log AS Value FROM temp_sql_log
UNION ALL
SELECT 'Service Queues' AS Source, queue AS Value FROM temp_service_queues;
