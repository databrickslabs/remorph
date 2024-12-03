--Query type: DDL
CREATE PARTITION FUNCTION pf_customer (INT) AS RANGE RIGHT FOR VALUES (1000, 2000, 3000, 4000);
CREATE PARTITION SCHEME ps_customer AS PARTITION pf_customer ALL TO ('customer1fg', 'customer2fg', 'customer3fg', 'customer4fg');
-- REMORPH CLEANUP: DROP PARTITION SCHEME ps_customer;
-- REMORPH CLEANUP: DROP PARTITION FUNCTION pf_customer;
