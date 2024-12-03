--Query type: DML
CREATE TABLE customer_target (c_custkey INT, c_acctbal DECIMAL(10, 2));

WITH derivedTable AS (
  SELECT c_custkey, MAX(o_totalprice) AS o_totalprice
  FROM orders
  GROUP BY c_custkey
)

MERGE INTO customer_target AS target
USING derivedTable AS source
ON target.c_custkey = source.c_custkey
WHEN MATCHED THEN
  UPDATE SET target.c_acctbal = source.o_totalprice
WHEN NOT MATCHED THEN
  INSERT (c_custkey, c_acctbal)
  VALUES (source.c_custkey, source.o_totalprice);

SELECT * FROM customer_target;
-- REMORPH CLEANUP: DROP TABLE customer_target;
