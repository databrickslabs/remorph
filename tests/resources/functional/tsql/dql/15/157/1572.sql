--Query type: DQL
DECLARE @orderkey INT = 1;
DECLARE @orderstatus CHAR(1) = 'O';
DECLARE @totalprice DECIMAL(12, 2) = 100.00;
SELECT CAST(@orderkey AS VARCHAR(10)) AS 'Order Key',
       CONVERT(CHAR(1), @orderstatus) AS 'Order Status',
       TRY_CAST(@totalprice AS DECIMAL(10, 2)) AS 'Total Price',
       TRY_CONVERT(CHAR(1), @orderstatus) AS 'Order Status',
       TRY_PARSE('2022-01-01' AS DATE) AS 'Order Date',
       PARSE('2022-01-01' AS DATE USING 'en-US') AS 'Order Date',
       FORMAT(@totalprice, 'C', 'en-US') AS 'Total Price';
