--Query type: DDL
DROP TABLE #TempTable;

WITH ordersCTE AS (
    SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment
    FROM (
        VALUES (1, 1, 'O', 100.0, '2020-01-01', 'LOW', 'John', 1, 'Comment1'),
               (2, 2, 'O', 200.0, '2020-01-02', 'MEDIUM', 'Jane', 2, 'Comment2')
    ) AS orders(o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment)
),

    customerCTE AS (
    SELECT c_custkey, c_name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS customer(c_custkey, c_name)
),

    TopOrders AS (
    SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment,
           ROW_NUMBER() OVER (ORDER BY o_totalprice DESC) AS RowNum
    FROM ordersCTE
)

SELECT to1.o_orderkey, to1.o_custkey, c2.c_name, to1.o_orderstatus, to1.o_totalprice, to1.o_orderdate, to1.o_orderpriority, to1.o_clerk, to1.o_shippriority, to1.o_comment
FROM TopOrders to1
JOIN customerCTE c2 ON to1.o_custkey = c2.c_custkey
WHERE to1.RowNum <= 10 AND to1.o_totalprice > (
    SELECT AVG(o_totalprice)
    FROM ordersCTE
)
GROUP BY to1.o_orderkey, to1.o_custkey, c2.c_name, to1.o_orderstatus, to1.o_totalprice, to1.o_orderdate, to1.o_orderpriority, to1.o_clerk, to1.o_shippriority, to1.o_comment
HAVING SUM(to1.o_totalprice) > (
    SELECT SUM(o_totalprice)
    FROM ordersCTE
    WHERE o_orderstatus = 'O'
);