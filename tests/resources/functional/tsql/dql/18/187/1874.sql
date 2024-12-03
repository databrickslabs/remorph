--Query type: DQL
DECLARE @orderdate smalldatetime = '1995-01-01 12:00:00';
DECLARE @ordertime time(4) = @orderdate;
WITH temp_result AS (
    SELECT @orderdate AS [Order Date], @ordertime AS [Order Time]
)
SELECT * FROM temp_result;
