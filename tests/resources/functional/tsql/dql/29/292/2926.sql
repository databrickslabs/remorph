--Query type: DQL
WITH customer AS (SELECT 'Customer#000000001' AS name, '1' AS c_custkey), orders AS (SELECT '1' AS o_orderkey, '1' AS o_custkey) SELECT c.name AS customer_name, o.o_orderkey AS order_key, TYPE_NAME(c.c_custkey) AS type_name FROM customer AS c INNER JOIN orders AS o ON c.c_custkey = o.o_custkey WHERE c.name = 'Customer#000000001' ORDER BY o.o_orderkey;
