-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

DECLARE @date DATETIME2 = '2020-04-30 21:21:21';
SELECT 'Week', DATE_BUCKET(WEEK, 1, @date)
UNION ALL
SELECT 'Day', DATE_BUCKET(DAY, 1, @date)
UNION ALL
SELECT 'Hour', DATE_BUCKET(HOUR, 1, @date)
UNION ALL
SELECT 'Minutes', DATE_BUCKET(MINUTE, 1, @date)
UNION ALL
SELECT 'Seconds', DATE_BUCKET(SECOND, 1, @date);