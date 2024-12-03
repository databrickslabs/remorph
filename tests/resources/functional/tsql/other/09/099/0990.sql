--Query type: DDL
SELECT * FROM (VALUES ('Supplier#000000001', 'USA', '123 Main St', '123-456-7890', 'This is a comment'), ('Supplier#000000002', 'Canada', '456 Elm St', '987-654-3210', 'This is another comment')) AS supplier (s_name, n_name, s_address, s_phone, s_comment);
