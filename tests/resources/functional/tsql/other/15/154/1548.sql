-- tsql sql:
DECLARE @d2 DATE, @t2 TIME, @dt2 DATETIME;
SET @d2 = GETDATE();
SET @t2 = GETDATE();
SET @dt2 = GETDATE();
SET @d2 = GETDATE();
SELECT *
FROM (
    VALUES (@d2, @t2, @dt2)
) AS temp_result(DateValue, TimeValue, DateTimeValue);
