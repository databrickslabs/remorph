-- tsql sql:
WITH Orders AS ( SELECT o_orderkey, o_totalprice FROM (VALUES (1, 10000.00), (2, 20000.00)) AS orders(o_orderkey, o_totalprice) ) SELECT [Result] = CASE WHEN o.o_totalprice > 10000 THEN 'High' ELSE 'Low' END FROM Orders o;
