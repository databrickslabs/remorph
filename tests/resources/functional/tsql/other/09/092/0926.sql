-- tsql sql:
CREATE DATABASE TestDB2;
CREATE TABLE customer
(
    custkey INT,
    name VARCHAR(100),
    nationkey INT
);
CREATE TABLE orders
(
    orderkey INT,
    custkey INT,
    orderdate DATE,
    totalprice DECIMAL(10, 2)
);
INSERT INTO customer (custkey, name, nationkey)
VALUES
    (1, 'Customer1', 1),
    (2, 'Customer2', 2);
INSERT INTO orders (orderkey, custkey, orderdate, totalprice)
VALUES
    (1, 1, '1995-01-01', 1000.00),
    (2, 1, '1995-01-02', 2000.00);
SELECT
    c.custkey,
    c.name,
    SUM(o.totalprice) AS total_order_value
FROM
    (
        VALUES
            (1, 'Customer1', 1),
            (2, 'Customer2', 2)
    ) c (custkey, name, nationkey)
    JOIN (
        VALUES
            (1, 1, '1995-01-01', 1000.00),
            (2, 1, '1995-01-02', 2000.00)
    ) o (orderkey, custkey, orderdate, totalprice)
    ON c.custkey = o.custkey
WHERE
    c.nationkey = 1
    AND o.orderdate >= '1995-01-01'
GROUP BY
    c.custkey,
    c.name
HAVING
    SUM(o.totalprice) > 100000
ORDER BY
    total_order_value DESC;
SELECT * FROM customer;
SELECT * FROM orders;
-- REMORPH CLEANUP: DROP TABLE customer;
-- REMORPH CLEANUP: DROP TABLE orders;
-- REMORPH CLEANUP: DROP DATABASE TestDB2;
