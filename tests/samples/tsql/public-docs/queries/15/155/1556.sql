-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

DECLARE @date DATETIME2 = '2020-04-15 21:22:11';
SELECT DATE_BUCKET(WEEK, 1, @date);