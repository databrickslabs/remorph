-- tsql sql:
SELECT supplier_name FROM (VALUES ('Supplier#000000001'), ('Supplier#000000002')) AS supplier (supplier_name) WHERE supplier_name LIKE 'Supplier#000000001' OR supplier_name LIKE 'Supplier#000000002'
