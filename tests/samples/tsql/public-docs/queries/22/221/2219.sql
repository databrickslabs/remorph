-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/kill-transact-sql?view=sql-server-ver16

KILL 54;  
KILL 54 WITH STATUSONLY;  
GO  
  
--This is the progress report.  
-- > spid 54: Transaction rollback in progress. Estimated rollback completion: 80% Estimated time left: 10 seconds.