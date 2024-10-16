--Query type: DML
WITH CustomerCTE AS (
  SELECT c_custkey, c_name
  FROM (
    VALUES (1, 'Customer1'), (2, 'Customer2'), (3, 'Customer3')
  ) AS Customer(c_custkey, c_name)
),
OrderCTE AS (
  SELECT o_orderkey, o_custkey, o_orderstatus
  FROM (
    VALUES (1, 1, 'O'), (2, 1, 'O'), (3, 2, 'O')
  ) AS Orders(o_orderkey, o_custkey, o_orderstatus)
)
SELECT c_custkey, c_name
INTO #CustomerResults
FROM CustomerCTE
WHERE c_custkey IN (SELECT o_custkey FROM OrderCTE WHERE o_orderstatus = 'O');

SELECT * FROM #CustomerResults;

DROP TABLE #CustomerResults;