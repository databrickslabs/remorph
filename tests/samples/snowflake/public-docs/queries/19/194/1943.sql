-- see https://docs.snowflake.com/en/sql-reference/account-usage

WITH
params AS (
SELECT
    CURRENT_WAREHOUSE() AS warehouse_name,
    '2021-11-01' AS time_from,
    '2021-11-02' AS time_to
),

jobs AS (
SELECT
    query_id,
    time_slice(start_time::timestamp_ntz, 15, 'minute','start') as interval_start,
    qh.warehouse_name,
    database_name,
    query_type,
    total_elapsed_time,
    compilation_time AS compilation_and_scheduling_time,
    (queued_provisioning_time + queued_repair_time + queued_overload_time) AS queued_time,
    transaction_blocked_time,
    execution_time
FROM snowflake.account_usage.query_history qh, params
WHERE
    qh.warehouse_name = params.warehouse_name
AND start_time >= params.time_from
AND start_time <= params.time_to
AND execution_status = 'SUCCESS'
AND query_type IN ('SELECT','UPDATE','INSERT','MERGE','DELETE')
),

interval_stats AS (
SELECT
    query_type,
    interval_start,
    COUNT(DISTINCT query_id) AS numjobs,
    MEDIAN(total_elapsed_time)/1000 AS p50_total_duration,
    (percentile_cont(0.95) within group (order by total_elapsed_time))/1000 AS p95_total_duration,
    SUM(total_elapsed_time)/1000 AS sum_total_duration,
    SUM(compilation_and_scheduling_time)/1000 AS sum_compilation_and_scheduling_time,
    SUM(queued_time)/1000 AS sum_queued_time,
    SUM(transaction_blocked_time)/1000 AS sum_transaction_blocked_time,
    SUM(execution_time)/1000 AS sum_execution_time,
    ROUND(sum_compilation_and_scheduling_time/sum_total_duration,2) AS compilation_and_scheduling_ratio,
    ROUND(sum_queued_time/sum_total_duration,2) AS queued_ratio,
    ROUND(sum_transaction_blocked_time/sum_total_duration,2) AS blocked_ratio,
    ROUND(sum_execution_time/sum_total_duration,2) AS execution_ratio,
    ROUND(sum_total_duration/numjobs,2) AS total_duration_perjob,
    ROUND(sum_compilation_and_scheduling_time/numjobs,2) AS compilation_and_scheduling_perjob,
    ROUND(sum_queued_time/numjobs,2) AS queued_perjob,
    ROUND(sum_transaction_blocked_time/numjobs,2) AS blocked_perjob,
    ROUND(sum_execution_time/numjobs,2) AS execution_perjob
FROM jobs
GROUP BY 1,2
ORDER BY 1,2
)
SELECT * FROM interval_stats;