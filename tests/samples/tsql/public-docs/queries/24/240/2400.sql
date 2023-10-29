-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/total-errors-transact-sql?view=sql-server-ver16

SELECT @@TOTAL_ERRORS AS 'Errors', GETDATE() AS 'As of';