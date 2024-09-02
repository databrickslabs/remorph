--Query type: DDL
CREATE PARTITION FUNCTION pf_orders_fact (date) AS RANGE RIGHT FOR VALUES ('1992-01-01', '1992-02-01', '1992-03-01', '1992-04-01', '1992-05-01', '1992-06-01', '1992-07-01', '1992-08-01', '1992-09-01', '1992-10-01', '1992-11-01', '1992-12-01', '1993-01-01', '1993-02-01', '1993-03-01', '1993-04-01', '1993-05-01', '1993-06-01', '1993-07-01', '1993-08-01', '1993-09-01', '1993-10-01', '1993-11-01', '1993-12-01', '1994-01-01', '1994-02-01', '1994-03-01', '1994-04-01', '1994-05-01', '1994-06-01', '1994-07-01', '1994-08-01', '1994-09-01', '1994-10-01', '1994-11-01', '1994-12-01');
CREATE PARTITION SCHEME ps_orders_fact AS PARTITION pf_orders_fact ALL TO ('PRIMARY');
CREATE TABLE orders_fact
(
    o_orderkey bigint,
    o_custkey bigint,
    o_orderstatus char(1),
    o_totalprice decimal(15, 2),
    o_orderdate date,
    o_orderpriority char(15),
    o_clerk char(15),
    o_shippriority int,
    o_comment varchar(79)
)
ON ps_orders_fact (o_orderdate);
CREATE CLUSTERED INDEX idx_orders_fact_o_orderdate ON orders_fact (o_orderdate);
-- REMORPH CLEANUP: DROP INDEX idx_orders_fact_o_orderdate ON orders_fact;
-- REMORPH CLEANUP: DROP TABLE orders_fact;
-- REMORPH CLEANUP: DROP PARTITION SCHEME ps_orders_fact;
-- REMORPH CLEANUP: DROP PARTITION FUNCTION pf_orders_fact;
SELECT * FROM orders_fact;