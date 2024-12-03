--Query type: DML
WITH OrdersCTE (orderkey, totalprice, orderdate) AS (
    SELECT orderkey, totalprice, orderdate
    FROM orders
    WHERE orderstatus = 'O'
),
OrderDetails (orderkey, totalprice, orderdate, quantity, extendedprice) AS (
    SELECT o.orderkey, o.totalprice, o.orderdate, l.quantity, l.extendedprice
    FROM OrdersCTE o
    INNER JOIN lineitem l ON o.orderkey = l.orderkey
    WHERE l.returnflag = 'R'
    UNION ALL
    SELECT o.orderkey, o.totalprice, o.orderdate, l.quantity, l.extendedprice
    FROM OrdersCTE o
    INNER JOIN lineitem l ON o.orderkey = l.orderkey
    WHERE l.quantity > 10
)
UPDATE o
SET totalprice = od.totalprice * 1.1
FROM orders o
JOIN OrderDetails od ON o.orderkey = od.orderkey;
