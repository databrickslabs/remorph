--Query type: DDL
CREATE DATABASE db_copy;
CREATE TABLE #customer
(
    id INT,
    name VARCHAR(100),
    amount DECIMAL(10, 2),
    address VARCHAR(200),
    phone VARCHAR(20),
    comment VARCHAR(200),
    nation_id INT
);
CREATE TABLE #orders
(
    id INT,
    customer_id INT,
    amount DECIMAL(10, 2)
);
CREATE TABLE #lineitem
(
    id INT,
    order_id INT,
    amount DECIMAL(10, 2),
    discount DECIMAL(5, 2),
    status CHAR(1)
);
CREATE TABLE #nation
(
    id INT,
    name VARCHAR(100)
);
INSERT INTO #nation (id, name)
VALUES (1, 'USA'),
       (2, 'Canada');
INSERT INTO #customer (id, name, amount, address, phone, comment, nation_id)
VALUES (1, 'Customer1', 100.0, '123 Main St', '123-456-7890', 'Comment1', 1),
       (2, 'Customer2', 200.0, '456 Elm St', '987-654-3210', 'Comment2', 2);
INSERT INTO #orders (id, customer_id, amount)
VALUES (1, 1, 100.0),
       (2, 1, 200.0),
       (3, 2, 50.0);
INSERT INTO #lineitem (id, order_id, amount, discount, status)
VALUES (1, 1, 10.0, 0.1, 'R'),
       (2, 1, 20.0, 0.2, 'R'),
       (3, 2, 30.0, 0.3, 'R');
SELECT *
FROM #customer;
SELECT *
FROM #orders;
SELECT *
FROM #lineitem;
SELECT *
FROM #nation;
-- REMORPH CLEANUP: DROP TABLE #customer;
-- REMORPH CLEANUP: DROP TABLE #orders;
-- REMORPH CLEANUP: DROP TABLE #lineitem;
-- REMORPH CLEANUP: DROP TABLE #nation;
-- REMORPH CLEANUP: DROP DATABASE db_copy;
