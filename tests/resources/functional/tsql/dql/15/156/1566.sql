--Query type: DQL
DECLARE @orderdate DATE = '1995-01-01';
DECLARE @linestatus VARCHAR(1) = 'O';
SELECT 'Order Date' = @orderdate, 'Line Status' = @linestatus
