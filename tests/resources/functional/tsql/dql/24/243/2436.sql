--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_nationkey, c_acctbal, c_mktsegment
    FROM (
        VALUES (1, 1, 100.0, 'BUILDING'),
               (2, 2, 200.0, 'AUTOMOBILE'),
               (3, 3, 300.0, 'MACHINERY')
    ) AS Customer(c_custkey, c_nationkey, c_acctbal, c_mktsegment)
),
RegionCTE AS (
    SELECT r_regionkey, r_name
    FROM (
        VALUES (1, 'ASIA'),
               (2, 'EUROPE'),
               (3, 'AFRICA')
    ) AS Region(r_regionkey, r_name)
)
SELECT c.c_custkey,
       r.r_regionkey,
       CONVERT(VARCHAR(20), c.c_acctbal, 1) AS c_acctbal,
       DATEPART(yy, '2022-01-01') AS OrderYear,
       CONVERT(VARCHAR(20), SUM(c.c_acctbal) OVER (PARTITION BY r.r_regionkey), 1) AS CumulativeTotal
FROM CustomerCTE c
INNER JOIN RegionCTE r ON c.c_nationkey = r.r_regionkey
WHERE r.r_regionkey IS NULL OR r.r_regionkey < 3;