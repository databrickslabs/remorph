--Query type: DQL
SELECT * FROM (VALUES ('customer', 'BASE TABLE')) AS temp_result (table_name, table_type) WHERE table_name = 'customer';