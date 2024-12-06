-- tsql sql:
SELECT supplier_name FROM (VALUES ('Supplier#000000001', 1), ('Supplier#000000002', 2)) AS suppliers (supplier_name, supplier_id) WHERE supplier_id = 1;
