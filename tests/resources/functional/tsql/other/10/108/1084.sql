--Query type: DML
DECLARE @OrderId INT;
WITH temp_result AS (
    SELECT 13 AS OrderId
)
SELECT @OrderId = OrderId
FROM temp_result;
EXEC uspDeleteOrder @OrderId = @OrderId;
SELECT * FROM Orders;