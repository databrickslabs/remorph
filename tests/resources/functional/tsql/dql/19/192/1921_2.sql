-- tsql sql:
DECLARE @orderDate VARCHAR(10) = '2022-01-01';
WITH temp AS (
    SELECT CONVERT(DATE, @orderDate) AS [OrderDateConversion]
)
SELECT * FROM temp;
