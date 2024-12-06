-- tsql sql:
WITH supplier_schema AS ( SELECT SCHEMA_NAME(schema_id) AS SchemaName, s_name FROM ( VALUES (1, 'Supplier#000000001'), (2, 'Supplier#000000002') ) AS suppliers (schema_id, s_name) ) SELECT SchemaName, s_name FROM supplier_schema ORDER BY SchemaName;
