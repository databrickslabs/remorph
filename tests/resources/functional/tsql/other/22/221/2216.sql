-- tsql sql:
CREATE TABLE #customer (c_custkey INT, c_name VARCHAR(25), c_address VARCHAR(40), c_nationkey INT, c_phone VARCHAR(15), c_acctbal DECIMAL(15, 2), c_mktsegment VARCHAR(10), c_comment VARCHAR(117));
CREATE TABLE #orders (o_orderkey INT, o_custkey INT, o_orderstatus VARCHAR(1), o_totalprice DECIMAL(15, 2), o_orderdate DATE, o_orderpriority VARCHAR(15), o_clerk VARCHAR(15), o_shippriority INT, o_comment VARCHAR(79));
WITH customer AS (
  SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
  FROM #customer
), orders AS (
  SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment
  FROM #orders
)
INSERT #customer (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
FROM customer
WHERE NOT EXISTS (
  SELECT c_custkey
  FROM orders o
  WHERE o.o_custkey = customer.c_custkey
);
SELECT * FROM #customer;
-- REMORPH CLEANUP: DROP TABLE #customer;
-- REMORPH CLEANUP: DROP TABLE #orders;
