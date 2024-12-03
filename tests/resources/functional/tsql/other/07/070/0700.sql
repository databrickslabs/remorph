--Query type: DML
CREATE TABLE customers (c_custkey INT, c_acctbal DECIMAL(10, 2));
CREATE TABLE orders (o_orderkey INT, o_custkey INT, o_orderstatus CHAR(1), o_totalprice DECIMAL(10, 2), o_orderdate DATE, o_orderpriority VARCHAR(10), o_clerk VARCHAR(20), o_shippriority INT, o_comment VARCHAR(50));
INSERT INTO orders (o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment)
VALUES (1, 1, 'O', 2100.00, '1996-03-13', '5-LOW', 'Clerk#000000001', 0, 'special   requests');
MERGE INTO customers c
USING (SELECT o_custkey, o_orderdate FROM orders WHERE DATEDIFF(day, CURRENT_DATE, o_orderdate) < -30) o
ON c.c_custkey = o.o_custkey
WHEN MATCHED THEN UPDATE SET c.c_acctbal = 40;
SELECT * FROM customers;
-- REMORPH CLEANUP: DROP TABLE customers;
-- REMORPH CLEANUP: DROP TABLE orders;
