--Query type: DDL
CREATE FUNCTION dbo.GetOrderInformation (@OrderKey INT)
RETURNS @retOrderInformation TABLE (
    OrderKey INT NOT NULL,
    OrderDate DATE NULL,
    TotalRevenue DECIMAL(10, 2) NULL,
    OrderStatus NVARCHAR(50) NULL,
    PRIMARY KEY CLUSTERED (OrderKey ASC)
)
AS
BEGIN
    DECLARE @OrderDate DATE, @TotalRevenue DECIMAL(10, 2), @OrderStatus NVARCHAR(50);

    WITH orders AS (
        SELECT o_orderkey, o_orderdate, SUM(ol_extendedprice * (1 - ol_discount)) AS TotalRevenue
        FROM (
            VALUES (1, '2020-01-01', 100.00, 0.1),
                   (2, '2020-01-02', 200.00, 0.2),
                   (3, '2020-01-03', 300.00, 0.3)
        ) AS orderlines (o_orderkey, o_orderdate, ol_extendedprice, ol_discount)
        GROUP BY o_orderkey, o_orderdate
    )
    SELECT @OrderKey = o_orderkey, @OrderDate = o_orderdate, @TotalRevenue = TotalRevenue
    FROM orders
    WHERE o_orderkey = @OrderKey;

    SET @OrderStatus = CASE
        WHEN EXISTS (
            SELECT *
            FROM (
                VALUES (1, 'Shipped'),
                       (2, 'Pending'),
                       (3, 'Delivered')
            ) AS orderstatus (o_orderkey, o_status)
            WHERE o_orderkey = @OrderKey AND o_status = 'Shipped'
        ) THEN 'Shipped'
        WHEN EXISTS (
            SELECT *
            FROM (
                VALUES (1, 'Shipped'),
                       (2, 'Pending'),
                       (3, 'Delivered')
            ) AS orderstatus (o_orderkey, o_status)
            WHERE o_orderkey = @OrderKey AND o_status = 'Pending'
        ) THEN 'Pending'
        WHEN EXISTS (
            SELECT *
            FROM (
                VALUES (1, 'Shipped'),
                       (2, 'Pending'),
                       (3, 'Delivered')
            ) AS orderstatus (o_orderkey, o_status)
            WHERE o_orderkey = @OrderKey AND o_status = 'Delivered'
        ) THEN 'Delivered'
    END;

    IF @OrderKey IS NOT NULL
    BEGIN
        INSERT @retOrderInformation
        SELECT @OrderKey, @OrderDate, @TotalRevenue, @OrderStatus;
    END;

    RETURN;
END;