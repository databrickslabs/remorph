-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

DECLARE @date DATETIME2 = '2020-06-15 21:22:11';
DECLARE @origin DATETIME2 = '2019-01-01 00:00:00';
SELECT DATE_BUCKET(WEEK, 5, @date, @origin);