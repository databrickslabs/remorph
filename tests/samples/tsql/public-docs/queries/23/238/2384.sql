-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cpu-busy-transact-sql?view=sql-server-ver16

SELECT @@CPU_BUSY * CAST(@@TIMETICKS AS FLOAT) AS 'CPU microseconds',   
   GETDATE() AS 'As of' ;