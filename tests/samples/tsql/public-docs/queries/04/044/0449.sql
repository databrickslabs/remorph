-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

--With resumable option; default locking behavior 
CREATE CLUSTERED INDEX idx_1 ON dbo.T2 (a) WITH (ONLINE = ON (WAIT_AT_LOW_PRIORITY (MAX_DURATION = 5 MINUTES, ABORT_AFTER_WAIT = NONE)), RESUMABLE = ON, MAX_DURATION = 240 MINUTES);