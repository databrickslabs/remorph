--Query type: DQL
SELECT c_custkey, c_name, c_nationkey FROM (VALUES (1, 'Customer#1', 1), (2, 'Customer#2', 2), (3, 'Customer#3', 3)) AS Customer(c_custkey, c_name, c_nationkey) ORDER BY c_custkey;