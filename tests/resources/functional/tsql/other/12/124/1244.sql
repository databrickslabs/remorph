-- tsql sql:
CREATE TABLE OrdersTable (o_orderkey INT, o_custkey INT, o_orderstatus AS (CASE WHEN o_orderkey > 1000 THEN 'HIGH' ELSE 'LOW' END) PERSISTED); -- REMORPH CLEANUP: DROP TABLE OrdersTable;
