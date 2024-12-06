-- tsql sql:
SELECT supplier_name, account_balance, nation_name AS nation FROM (VALUES ('Supplier#000000001', 5000.0, 'UNITED STATES'), ('Supplier#000000002', 10000.0, 'UNITED KINGDOM')) AS suppliers (supplier_name, account_balance, nation_name) ORDER BY supplier_name ASC;
