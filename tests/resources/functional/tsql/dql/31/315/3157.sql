--Query type: DQL
WITH CustomerCTE AS (SELECT 'Customer#000000001' AS c_name, 1 AS c_custkey), OrdersCTE AS (SELECT 'Order#000000001' AS o_orderkey, 1 AS o_custkey) SELECT DISTINCT c_name FROM CustomerCTE AS c WHERE EXISTS (SELECT * FROM OrdersCTE AS o WHERE c.c_custkey = o.o_custkey AND o.o_orderkey LIKE 'Order#000000001%');
