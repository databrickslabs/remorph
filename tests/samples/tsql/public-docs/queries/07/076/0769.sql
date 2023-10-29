-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-workload-group-transact-sql?view=sql-server-ver16

ALTER WORKLOAD GROUP "default"
WITH (IMPORTANCE = LOW);
GO
ALTER RESOURCE GOVERNOR RECONFIGURE;
GO