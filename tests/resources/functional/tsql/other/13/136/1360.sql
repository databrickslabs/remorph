-- tsql sql:
CREATE VIEW Sales.SalesReject
WITH ENCRYPTION
AS
    SELECT
        OrderKey,
        ExtendedPrice,
        Discount,
        ExtendedPrice * (1 - Discount) AS NetPrice,
        ShipDate
    FROM
    (
        VALUES
            (1, 100.0, 0.1, '2020-01-01'),
            (2, 200.0, 0.2, '2020-01-15')
    ) AS Sales (
        OrderKey,
        ExtendedPrice,
        Discount,
        ShipDate
    )
    WHERE
        ExtendedPrice * (1 - Discount) > 50
        AND ShipDate > CONVERT(DATETIME, '20200101', 101);
-- REMORPH CLEANUP: DROP VIEW Sales.SalesReject;
