-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

DECLARE @date DATETIME2 = '2020-04-30 00:00:00';
SELECT DATE_BUCKET(DAY, 2147483648, @date);