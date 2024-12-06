-- tsql sql:
DECLARE @customer_orders TABLE (c_custkey INT, c_name VARCHAR(50), o_orderkey INT, o_totalprice DECIMAL(10, 2));
INSERT INTO @customer_orders (c_custkey, c_name, o_orderkey, o_totalprice)
SELECT c.c_custkey, c.c_name, o.o_orderkey, o.o_totalprice
FROM (VALUES (1, 'Customer 1', 1, 100.00), (2, 'Customer 2', 2, 200.00), (3, 'Customer 3', 3, 300.00)) c (c_custkey, c_name, o_orderkey, o_totalprice)
INNER JOIN (VALUES (1, 1, 'O', 100.00), (2, 1, 'O', 200.00), (3, 2, 'O', 300.00)) o (o_orderkey, o_custkey, o_orderstatus, o_totalprice)
ON c.c_custkey = o.o_custkey;
DELETE co
FROM @customer_orders co
WHERE EXISTS (
    SELECT TOP 1 1
    FROM (VALUES (1, 1, 'O', 100.00), (2, 1, 'O', 200.00), (3, 2, 'O', 300.00)) o (o_orderkey, o_custkey, o_orderstatus, o_totalprice)
    WHERE o.o_custkey = co.c_custkey AND o.o_totalprice > 200.00
);
SELECT * FROM @customer_orders;
