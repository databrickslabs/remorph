--Query type: DQL
DECLARE @orderdate smalldatetime = '1995-01-01 12:00:00';
DECLARE @shipdate datetime = @orderdate;
SELECT orderdate, shipdate
FROM (
    VALUES (@orderdate, @shipdate)
) AS temp_result(orderdate, shipdate);