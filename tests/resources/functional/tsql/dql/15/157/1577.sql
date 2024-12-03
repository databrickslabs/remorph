--Query type: DQL
DECLARE @orderdate datetimeoffset(4) = '1995-03-01 12:00:00.0000 +00:00';
DECLARE @shipdate datetimeoffset(4) = @orderdate;
SELECT *
FROM (
    VALUES (@orderdate, @shipdate)
) AS temp_result (OrderDate, ShipDate);
