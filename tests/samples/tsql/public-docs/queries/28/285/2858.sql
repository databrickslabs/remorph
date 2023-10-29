-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showexecutionplan-transact-sql?view=aps-pdw-2016-au7

SELECT [sql_spid]
    , [pdw_node_id]
    , [request_id]
    , [dms_step_index]
    , [type]
    , [start_time]
    , [end_time]
    , [status]
FROM sys.dm_pdw_dms_workers
WHERE [status] <> 'StepComplete'
    AND [status] <> 'StepError'
    AND pdw_node_id = 201001
ORDER BY request_id
    , [dms_step_index]
    , [distribution_id];