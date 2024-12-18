-- tsql sql:
CREATE PROCEDURE Sales.Update_OrderKey
    @NewKey INTEGER
AS
BEGIN
    SET NOCOUNT ON;

    WITH OrdersCTE AS (
        SELECT l_orderkey, l_extendedprice, l_discount
        FROM (
            VALUES (1, 100.00, 0.1),
                   (2, 200.00, 0.2),
                   (3, 300.00, 0.3)
        ) AS Orders(l_orderkey, l_extendedprice, l_discount)
    )
    SELECT CASE WHEN l_discount > 0.1 THEN l_orderkey + @NewKey ELSE @NewKey END AS New_l_orderkey,
           l_extendedprice,
           l_discount
    INTO #UpdatedOrders
    FROM OrdersCTE
    WHERE l_extendedprice > 200.00;

    SELECT * FROM #UpdatedOrders;
END;
-- REMORPH CLEANUP: DROP TABLE #UpdatedOrders;
-- REMORPH CLEANUP: DROP PROCEDURE Sales.Update_OrderKey;
