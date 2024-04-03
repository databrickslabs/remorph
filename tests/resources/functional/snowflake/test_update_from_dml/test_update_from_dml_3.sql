
-- source:
UPDATE orders t1
                            SET order_status = 'returned'
                            WHERE EXISTS (SELECT oid FROM returned_orders WHERE t1.oid = oid);

-- databricks_sql:
UPDATE orders AS t1 SET order_status = 'returned' WHERE EXISTS(SELECT oid FROM returned_orders WHERE t1.oid = oid);
