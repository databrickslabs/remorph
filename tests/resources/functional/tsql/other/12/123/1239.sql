-- tsql sql:
CREATE TABLE Tbl ( id INT PRIMARY KEY, o_orderkey INT, l_extendedprice DECIMAL(10, 2), o_totalprice DECIMAL(10, 2) );
WITH orders AS (
    SELECT 1 AS o_orderkey, 10.0 AS o_totalprice, 100.0 AS l_extendedprice
    UNION ALL
    SELECT 1 AS o_orderkey, 20.0 AS o_totalprice, 200.0 AS l_extendedprice
    UNION ALL
    SELECT 2 AS o_orderkey, 30.0 AS o_totalprice, 300.0 AS l_extendedprice
),
lineitem AS (
    SELECT 1 AS o_orderkey, 1000.0 AS l_extendedprice
    UNION ALL
    SELECT 2 AS o_orderkey, 2000.0 AS l_extendedprice
)
INSERT INTO Tbl (o_orderkey, l_extendedprice, o_totalprice)
SELECT orders.o_orderkey, lineitem.l_extendedprice, orders.o_totalprice
FROM orders
INNER JOIN lineitem ON orders.o_orderkey = lineitem.o_orderkey;
SELECT * FROM Tbl;
-- REMORPH CLEANUP: DROP TABLE Tbl;
