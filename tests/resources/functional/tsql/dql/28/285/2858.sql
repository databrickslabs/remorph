--Query type: DQL
WITH temp_result AS (
    SELECT 1 AS sql_spid, 201001 AS pdw_node_id, 1 AS request_id, 1 AS dms_step_index, 'type' AS type, '2022-01-01' AS start_time, '2022-01-01' AS end_time, 'status' AS status
    UNION ALL
    SELECT 2, 201001, 2, 2, 'type', '2022-01-01', '2022-01-01', 'status'
)
SELECT sql_spid, pdw_node_id, request_id, dms_step_index, type, start_time, end_time, status
FROM temp_result
WHERE status <> 'StepComplete' AND status <> 'StepError' AND pdw_node_id = 201001
ORDER BY request_id, dms_step_index, pdw_node_id
