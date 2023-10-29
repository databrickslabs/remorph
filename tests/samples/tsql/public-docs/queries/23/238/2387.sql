-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/io-busy-transact-sql?view=sql-server-ver16

SELECT @@IO_BUSY*@@TIMETICKS AS 'IO microseconds',   
   GETDATE() AS 'as of';