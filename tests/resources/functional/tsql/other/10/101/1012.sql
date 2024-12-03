--Query type: DDL
CREATE FUNCTION Region.ufn_SalesByRegion (@regionid int)
RETURNS TABLE
AS
RETURN (
    SELECT T1.ProductID, T1.ProductName, SUM(T2.ExtendedPrice) AS 'Total'
    FROM (
        VALUES (1, 'Product A'),
               (2, 'Product B'),
               (3, 'Product C')
    ) AS T1 (ProductID, ProductName)
    JOIN (
        VALUES (1, 1, 10.0),
               (1, 2, 20.0),
               (2, 1, 30.0),
               (2, 2, 40.0),
               (3, 1, 50.0),
               (3, 2, 60.0)
    ) AS T2 (ProductID, OrderID, ExtendedPrice)
        ON T2.ProductID = T1.ProductID
    JOIN (
        VALUES (1, 1),
               (2, 1),
               (3, 2)
    ) AS T3 (OrderID, RegionID)
        ON T3.OrderID = T2.OrderID
    WHERE T3.RegionID = @regionid
    GROUP BY T1.ProductID, T1.ProductName
);
