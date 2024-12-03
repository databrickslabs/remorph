--Query type: DQL
SELECT r_name, c_custkey, c_acctbal, LAG(c_acctbal, 1, 0) OVER (PARTITION BY r_name ORDER BY c_acctbal DESC) AS PrevAcctBal FROM (VALUES ('USA', 1, 100.0), ('USA', 2, 200.0), ('Canada', 3, 300.0), ('Canada', 4, 400.0)) AS Customer(r_name, c_custkey, c_acctbal) WHERE r_name IN ('USA', 'Canada') ORDER BY r_name
