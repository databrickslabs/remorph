-- tsql sql:
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dbo')
BEGIN
    EXEC('CREATE SCHEMA dbo');
END;

-- Revoke control on schema
REVOKE CONTROL ON SCHEMA::dbo FROM RolandX;

-- Main query using CTEs
WITH customer AS (
    SELECT * FROM (VALUES
        (1, 'Customer1', 1),
        (2, 'Customer2', 2)
    ) AS customer(custkey, name, nationkey)
),
orders AS (
    SELECT * FROM (VALUES
        (1, 1, '1995-01-01', 1000.0),
        (2, 1, '1995-01-02', 2000.0)
    ) AS orders(orderkey, custkey, orderdate, totalprice)
)
SELECT TOP 10 c.custkey, c.name, SUM(o.totalprice) AS total_revenue
FROM customer c
JOIN orders o ON c.custkey = o.custkey
WHERE c.nationkey = 1 AND o.orderdate >= '1995-01-01'
GROUP BY c.custkey, c.name
HAVING SUM(o.totalprice) > 1000000
ORDER BY total_revenue DESC;

-- REMORPH CLEANUP: DROP SCHEMA dbo;
