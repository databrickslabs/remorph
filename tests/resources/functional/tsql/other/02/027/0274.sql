-- tsql sql:
CREATE PROCEDURE calculate_total_revenue
AS
BEGIN
    WITH lineitem AS (
        SELECT 1 AS l_extendedprice, 0.5 AS l_discount
        UNION ALL
        SELECT 2, 0.3
        UNION ALL
        SELECT 3, 0.2
    )
    SELECT SUM(l_extendedprice * l_discount) AS TotalRevenue
    FROM lineitem;
END;

-- Execute the stored procedure
EXEC calculate_total_revenue;

-- REMORPH CLEANUP: DROP PROCEDURE calculate_total_revenue;
