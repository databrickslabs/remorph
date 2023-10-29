-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-workload-group-transact-sql?view=sql-server-ver16

CREATE WORKLOAD GROUP newReports
WITH
    (REQUEST_MAX_MEMORY_GRANT_PERCENT = 2.5
      , REQUEST_MAX_CPU_TIME_SEC = 100
      , MAX_DOP = 4)
USING "default" ;
GO