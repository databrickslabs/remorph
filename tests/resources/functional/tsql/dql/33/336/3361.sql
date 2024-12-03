--Query type: DQL
SELECT supplier_name, account_balance FROM (VALUES ('Supplier#000000001', 1000.0), ('Supplier#000000002', NULL)) AS supplier (supplier_name, account_balance) WHERE account_balance IS NULL;
