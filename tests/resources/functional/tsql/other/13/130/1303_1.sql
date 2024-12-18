-- tsql sql:
INSERT INTO orders (orderkey, orderdate, extendedprice)
SELECT orderkey, orderdate, extendedprice
FROM (
    VALUES (1, '2022-01-01', 100.0),
           (2, '2022-01-02', 200.0)
) AS sales (orderkey, orderdate, extendedprice);
