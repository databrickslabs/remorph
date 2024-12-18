-- tsql sql:
CREATE PARTITION FUNCTION pf_orders (INT) AS RANGE LEFT FOR VALUES (100, 1000, 10000);
CREATE PARTITION SCHEME ps_orders AS PARTITION pf_orders TO (customer_fg, orders_fg, lineitem_fg, supplier_fg);
-- REMORPH CLEANUP: DROP PARTITION SCHEME ps_orders;
-- REMORPH CLEANUP: DROP PARTITION FUNCTION pf_orders;
