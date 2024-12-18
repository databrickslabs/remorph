-- tsql sql:
CREATE TABLE #tmp_orders (o_orderkey INT, o_custkey INT, o_orderstatus CHAR(1));
INSERT INTO #tmp_orders VALUES (1, 1, 'O');
INSERT INTO #tmp_orders VALUES (2, 2, 'O');
WITH tmp AS (
    SELECT * FROM #tmp_orders
)
SELECT o_orderkey, o_custkey, o_orderstatus FROM tmp;
