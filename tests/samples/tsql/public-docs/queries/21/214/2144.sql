-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/trigger-nestlevel-transact-sql?view=sql-server-ver16

IF ( ( SELECT TRIGGER_NESTLEVEL ( ( SELECT object_id FROM sys.triggers  
WHERE name = 'abc' ), 'AFTER' , 'DDL' ) ) > 5 )  
   RAISERROR ('Trigger abc nested more than 5 levels.',16,-1)