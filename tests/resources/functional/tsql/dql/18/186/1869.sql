--Query type: DQL
DECLARE @orderdate DATE = '1995-01-01';
DECLARE @linestatus CHAR(1) = 'O';
SELECT *
FROM (
    VALUES (@orderdate, @linestatus)
) AS temp_result (OrderDate, LineStatus);
