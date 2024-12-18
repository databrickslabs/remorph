-- tsql sql:
CREATE PROCEDURE DaysToShip
    @OrderKey INT,
    @LineStatus VARCHAR(10)
AS
BEGIN
    WITH OrdersCTE AS (
        SELECT OrderKey, LineStatus, OrderDate, ShipDate
        FROM (
            VALUES (1, 'O', '2020-01-01', '2020-01-10'),
                   (2, 'O', '2020-01-15', '2020-01-25'),
                   (3, 'P', '2020-02-01', '2020-02-10')
        ) AS Orders(OrderKey, LineStatus, OrderDate, ShipDate)
    )
    SELECT DATEDIFF(day, OrderDate, ShipDate) AS DaysToShip
    FROM OrdersCTE
    WHERE OrderKey = @OrderKey AND LineStatus = @LineStatus;
END
EXECUTE DaysToShip 1, 'O';
-- REMORPH CLEANUP: DROP PROCEDURE DaysToShip;
