--Query type: DDL
CREATE VIEW V2 AS SELECT l_orderkey, l_extendedprice FROM (VALUES (1, 10.0), (2, 20.0), (3, 30.0)) AS T2 (l_orderkey, l_extendedprice);