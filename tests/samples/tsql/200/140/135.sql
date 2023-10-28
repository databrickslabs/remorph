USE master;
GO

SELECT dbid,
    object_id,
    query_plan
FROM sys.dm_exec_cached_plans AS cp
CROSS APPLY sys.dm_exec_query_plan(cp.plan_handle);
GO