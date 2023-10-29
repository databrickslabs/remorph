-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/idle-transact-sql?view=sql-server-ver16

SELECT @@IDLE * CAST(@@TIMETICKS AS float) AS 'Idle microseconds',  
   GETDATE() AS 'as of';