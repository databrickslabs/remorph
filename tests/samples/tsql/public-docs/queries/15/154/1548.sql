-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

DECLARE @d1 DATE,
    @t1 TIME,
    @dt1 DATETIME;

SET @d1 = GETDATE();
SET @t1 = GETDATE();
SET @dt1 = GETDATE();
SET @d1 = GETDATE();

-- When converting date to datetime the minutes portion becomes zero.
SELECT @d1 AS [DATE],
    CAST(@d1 AS DATETIME) AS [date as datetime];

-- When converting time to datetime the date portion becomes zero
-- which converts to January 1, 1900.
SELECT @t1 AS [TIME],
    CAST(@t1 AS DATETIME) AS [time as datetime];

-- When converting datetime to date or time non-applicable portion is dropped.
SELECT @dt1 AS [DATETIME],
    CAST(@dt1 AS DATE) AS [datetime as date],
    CAST(@dt1 AS TIME) AS [datetime as time];