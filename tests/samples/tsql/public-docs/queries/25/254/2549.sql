-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

SELECT DATE_BUCKET(DAY, 10, SYSUTCDATETIME());