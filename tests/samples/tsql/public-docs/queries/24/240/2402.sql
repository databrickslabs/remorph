-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/total-read-transact-sql?view=sql-server-ver16

SELECT @@TOTAL_READ AS 'Reads', @@TOTAL_WRITE AS 'Writes', GETDATE() AS 'As of';