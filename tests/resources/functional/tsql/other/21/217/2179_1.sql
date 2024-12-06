-- tsql sql:
CREATE PROCEDURE dbo.uspCustomerByRegion
    @Region VARCHAR(25) = '%'
WITH RECOMPILE
AS
SET NOCOUNT ON;

WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_nationkey
    FROM (
        VALUES (1, 'Customer#000000001', 1),
               (2, 'Customer#000000002', 2),
               (3, 'Customer#000000003', 3)
    ) AS Customer(c_custkey, c_name, c_nationkey)
),
RegionCTE AS (
    SELECT r_regionkey, r_name
    FROM (
        VALUES (1, 'AFRICA'),
               (2, 'ASIA'),
               (3, 'EUROPE')
    ) AS Region(r_regionkey, r_name)
),
NationCTE AS (
    SELECT n_nationkey, n_name, n_regionkey
    FROM (
        VALUES (1, 'ALGERIA', 0),
               (2, 'ARGENTINA', 1),
               (3, 'AUSTRALIA', 3)
    ) AS Nation(n_nationkey, n_name, n_regionkey)
)
SELECT c.c_name AS 'Customer name', r.r_name AS 'Region name'
FROM CustomerCTE c
JOIN NationCTE n ON c.c_nationkey = n.n_nationkey
JOIN RegionCTE r ON n.n_regionkey = r.r_regionkey
WHERE r.r_name LIKE @Region;
