-- tsql sql:
CREATE TABLE t1 WITH (DISTRIBUTION = ROUND_ROBIN) AS SELECT * FROM (VALUES ('customer_name', 'customer_address', 'customer_phone', 0.00, '1900-01-01', 0.00, 'nation_name', 'region_name', 'part_name', 'part_mfgr', 'part_brand', 'part_type', 0, 'part_container', 0.00, 'part_comment', 'supplier_name', 'supplier_address', 'supplier_phone', 0.00, '1900-01-01', 0.00, 'O', 0.00, '1900-01-01', 0, 0, 0.00, 0.00, 0.00)) AS temp_result(customer_name, customer_address, customer_phone, customer_account_balance, customer_since, customer_credit_limit, nation_name, region_name, part_name, part_mfgr, part_brand, part_type, part_size, part_container, part_retail_price, part_comment, supplier_name, supplier_address, supplier_phone, supplier_account_balance, supplier_since, supplier_credit_limit, orders_order_status, orders_total_price, orders_order_date, orders_ship_priority, lineitem_quantity, lineitem_extended_price, lineitem_discount, lineitem_tax);