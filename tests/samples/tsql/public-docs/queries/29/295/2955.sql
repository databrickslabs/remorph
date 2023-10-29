-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-result-set-caching-transact-sql?view=azure-sqldw-latest

SELECT result_cache_hit
FROM sys.dm_pdw_exec_requests
WHERE request_id = 'QID58286'