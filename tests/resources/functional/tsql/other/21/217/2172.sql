--Query type: DDL
CREATE PROCEDURE Sales.uspGetOrders
    @OrderDate DATE = '1995-01-01',
    @TotalPrice DECIMAL(10, 2) = 100.00
AS
    SET NOCOUNT ON;
    WITH OrdersCTE AS (
        SELECT 'Order1' AS OrderName, '1995-01-01' AS OrderDate, 100.00 AS TotalPrice
        UNION ALL
        SELECT 'Order2', '1995-01-02', 200.00
    )
    SELECT OrderName, OrderDate, TotalPrice
    FROM OrdersCTE
    WHERE OrderDate >= @OrderDate AND TotalPrice > @TotalPrice;