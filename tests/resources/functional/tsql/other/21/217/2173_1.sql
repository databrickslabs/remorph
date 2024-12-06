-- tsql sql:
CREATE PROCEDURE Sales.uspGetOrderList
    @Customer VARCHAR(40),
    @MaxTotal MONEY,
    @CompareTotal MONEY OUTPUT,
    @Total MONEY OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    WITH CustomerOrders AS (
        SELECT c.c_name AS Customer, o.o_totalprice AS Total
        FROM (
            VALUES ('Customer#0001', 100.00),
                   ('Customer#0002', 200.00)
        ) AS c (c_name, c_acctbal)
        JOIN (
            VALUES ('Order#0001', 'Customer#0001', 100.00),
                   ('Order#0002', 'Customer#0002', 200.00)
        ) AS o (o_orderkey, o_custkey, o_totalprice)
        ON c.c_name = o.o_custkey
    )
    SELECT Customer, Total AS 'Order Total'
    FROM CustomerOrders
    WHERE Customer LIKE @Customer AND Total < @MaxTotal;

    SET @Total = (SELECT MAX(Total) FROM CustomerOrders WHERE Customer LIKE @Customer AND Total < @MaxTotal);
    SET @CompareTotal = @MaxTotal;
END;
-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspGetOrderList;
