-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-workload-group-transact-sql?view=sql-server-ver16

SELECT *
FROM sys.workload_management_workload_groups
WHERE [name] = 'wgDataLoads'

ALTER WORKLOAD GROUP wgDataLoads WITH
( MIN_PERCENTAGE_RESOURCE            = 40
, CAP_PERCENTAGE_RESOURCE            = 80
, REQUEST_MIN_RESOURCE_GRANT_PERCENT = 10 )