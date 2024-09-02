--Query type: DQL
DECLARE @orderdate datetimeoffset(7) = '2016-10-23 12:45:37.1234567 +10:0';
DECLARE @shipdate datetime2 = CAST(@orderdate AS datetime2);
WITH cte AS (
    SELECT @shipdate AS shipdate, @orderdate AS orderdate
)
SELECT * FROM cte;