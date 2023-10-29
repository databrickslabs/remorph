-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/trigger-nestlevel-transact-sql?view=sql-server-ver16

IF ( (SELECT TRIGGER_NESTLEVEL( OBJECT_ID('xyz') , 'AFTER' , 'DML' ) ) > 5 )  
   RAISERROR('Trigger xyz nested more than 5 levels.',16,-1)