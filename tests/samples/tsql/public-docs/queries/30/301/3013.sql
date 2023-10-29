-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/lock-timeout-transact-sql?view=sql-server-ver16

SET LOCK_TIMEOUT 1800;  
SELECT @@LOCK_TIMEOUT AS [Lock Timeout];  
GO