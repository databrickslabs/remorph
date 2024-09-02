--Query type: DML
DECLARE @newdate DATETIME, @addhours INT;
SET @newdate = 'January 15, 1900 12:00 AM';
SET @addhours = 5;
WITH temp_result AS (
    SELECT @newdate + 1.25 AS [New Date], @newdate + @addhours AS [Add Hours]
)
SELECT * FROM temp_result;