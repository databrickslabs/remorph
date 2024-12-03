--Query type: DDL
CREATE TABLE supplier_lineitem (
    sl_orderkey INT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
    sl_suppkey INT,
    sl_extendedprice DECIMAL(10, 2)
);

WITH supplier_data AS (
    SELECT s_suppkey, s_nationkey, s_acctbal
    FROM (
        VALUES (1, 1, 100.0),
               (2, 2, 200.0),
               (3, 3, 300.0)
    ) AS supplier (s_suppkey, s_nationkey, s_acctbal)
),
lineitem_data AS (
    SELECT l_orderkey, l_suppkey, l_extendedprice
    FROM (
        VALUES (1, 1, 1000.0),
               (2, 2, 2000.0),
               (3, 3, 3000.0)
    ) AS lineitem (l_orderkey, l_suppkey, l_extendedprice)
)
INSERT INTO supplier_lineitem (sl_suppkey, sl_extendedprice)
SELECT s.s_suppkey, l.l_extendedprice
FROM supplier_data s
INNER JOIN lineitem_data l ON s.s_suppkey = l.l_suppkey;

SELECT * FROM supplier_lineitem;
-- REMORPH CLEANUP: DROP TABLE supplier_lineitem;
