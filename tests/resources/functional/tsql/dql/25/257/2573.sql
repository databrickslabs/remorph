-- tsql sql:
WITH SalesRegion AS (
    SELECT DISTINCT r_name, r_regionkey
    FROM region
),
SalesNation AS (
    SELECT DISTINCT n_name, n_nationkey
    FROM nation
),
SalesCustomer AS (
    SELECT DISTINCT c_name, c_nationkey, c_custkey
    FROM customer
)
SELECT DISTINCT sr.r_name,
    MIN(sc.c_acctbal) OVER (PARTITION BY sn.n_nationkey) AS MinBalance,
    MAX(sc.c_acctbal) OVER (PARTITION BY sn.n_nationkey) AS MaxBalance,
    AVG(sc.c_acctbal) OVER (PARTITION BY sn.n_nationkey) AS AvgBalance,
    COUNT(sc.c_custkey) OVER (PARTITION BY sn.n_nationkey) AS CustomersPerNation
FROM SalesRegion sr
JOIN SalesNation sn ON sr.r_regionkey = sn.n_regionkey
JOIN SalesCustomer sc ON sn.n_nationkey = sc.c_nationkey
WHERE sc.c_acctbal > 0
ORDER BY sr.r_name;
