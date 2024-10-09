--Query type: DML
CREATE TABLE #orders
(
    o_orderkey INT,
    o_custkey INT,
    o_totalprice DECIMAL(10, 2)
);

CREATE TABLE #customers
(
    c_custkey INT,
    c_acctbal DECIMAL(10, 2)
);

INSERT INTO #orders (o_orderkey, o_custkey, o_totalprice)
VALUES
    (1, 1, 100.00),
    (2, 2, 200.00),
    (3, 3, 300.00);

INSERT INTO #customers (c_custkey, c_acctbal)
VALUES
    (1, 1000.00),
    (2, 2000.00),
    (3, 3000.00);

DECLARE ord_cursor CURSOR LOCAL FOR
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM #orders
    WHERE o_orderkey = 1;

OPEN ord_cursor;

DECLARE @o_orderkey INT, @o_custkey INT, @o_totalprice DECIMAL(10, 2);

FETCH NEXT FROM ord_cursor INTO @o_orderkey, @o_custkey, @o_totalprice;

UPDATE o
SET o.o_totalprice = o.o_totalprice + c.c_acctbal
FROM #orders o
INNER JOIN #customers c ON c.c_custkey = o.o_custkey
WHERE o.o_orderkey = @o_orderkey AND c.c_custkey = o.o_custkey;

CLOSE ord_cursor;

DEALLOCATE ord_cursor;

SELECT * FROM #orders;