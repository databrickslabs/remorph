-- tsql sql:
WITH vw_CustomerOrders AS ( SELECT c_custkey, c_name, o_orderkey, o_orderdate FROM ( VALUES (1, 'Customer1', 1, '2020-01-01'), (2, 'Customer2', 2, '2020-01-02') ) AS c ( c_custkey, c_name, o_orderkey, o_orderdate ) ) SELECT * FROM vw_CustomerOrders;
