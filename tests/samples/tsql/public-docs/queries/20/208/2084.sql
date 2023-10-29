-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-query?view=sql-server-ver16

EXEC sys.sp_query_store_set_hints @query_id= 39, @query_hints = N'OPTION(MAX_GRANT_PERCENT=10)';