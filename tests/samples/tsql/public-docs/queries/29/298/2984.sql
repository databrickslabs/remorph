-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-traceon-trace-flags-transact-sql?view=sql-server-ver16

SELECT x FROM correlated WHERE f1 = 0 AND f2 = 1 OPTION (QUERYTRACEON 4199, QUERYTRACEON 4137);