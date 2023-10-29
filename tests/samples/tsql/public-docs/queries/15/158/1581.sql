-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16

DECLARE @days INT = 365,
    @datetime DATETIME2 = '2000-01-01 01:01:01.1110000';
    /* 2000 was a leap year */;
SELECT DATE_BUCKET(DAY, @days, @datetime);