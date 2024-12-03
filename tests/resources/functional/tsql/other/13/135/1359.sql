--Query type: DDL
CREATE VIEW CustomerOrderDates AS SELECT c_name, o_orderdate FROM (VALUES ('Customer#000000001', '1996-01-02'), ('Customer#000000002', '1996-01-03')) AS CustomerOrders (c_name, o_orderdate);
