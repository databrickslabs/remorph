-- tsql sql:
DECLARE @orderdate smalldatetime = '1995-01-01 12:00:00';
DECLARE @shipdate date = @orderdate;

WITH temp_result AS (
    SELECT @orderdate AS orderdate, @shipdate AS shipdate
)
SELECT * FROM temp_result;
