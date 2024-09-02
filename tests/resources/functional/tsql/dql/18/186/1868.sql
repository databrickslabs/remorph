--Query type: DQL
DECLARE @orderdate DATE = '1995-01-01';
DECLARE @shipdate DATETIME2 = @orderdate;
SELECT *
FROM (
    VALUES (@shipdate, @orderdate)
) AS temp_result (shipdate, orderdate);