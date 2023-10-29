-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-sqlperf-transact-sql?view=sql-server-ver16

DBCC SQLPERF ("sys.dm_os_wait_stats", CLEAR);