-- tsql sql:
CREATE PROCEDURE Sales.uspGetCustomers
    @CustomerName NVARCHAR(50),
    @Country NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    WITH CustomerCTE AS (
        SELECT c_custkey, c_name, c_nationkey, c_phone
        FROM (
            VALUES
                (1, 'Customer#001', 1, '123-456-7890'),
                (2, 'Customer#002', 2, '987-654-3210'),
                (3, 'Customer#003', 3, '555-123-4567')
        ) AS Customer(c_custkey, c_name, c_nationkey, c_phone)
    )
    SELECT c_name, c_phone, n_name
    FROM CustomerCTE
    JOIN (
        VALUES
            (1, 'Nation#001'),
            (2, 'Nation#002'),
            (3, 'Nation#003')
    ) AS Nation(n_nationkey, n_name) ON CustomerCTE.c_nationkey = Nation.n_nationkey
    WHERE c_name = @CustomerName AND n_name = @Country;
END;
-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspGetCustomers;
