--Query type: DML
CREATE TABLE customer_orders (order_total DECIMAL(10, 2));
INSERT INTO customer_orders (order_total)
  SELECT drvd.[NewTotal]
  FROM   (VALUES (100.00), (200.00), (300.00), (400.00), (500.00)) drvd([NewTotal]);
-- REMORPH CLEANUP: DROP TABLE customer_orders;
