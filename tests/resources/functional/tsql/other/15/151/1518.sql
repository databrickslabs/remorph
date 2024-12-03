--Query type: DCL
SELECT * FROM (VALUES (1, 'John', 100.00, 'USA', '123 Main St', '123-456-7890', 'Good customer'), (2, 'Jane', 200.00, 'Canada', '456 Elm St', '987-654-3210', 'Bad customer')) AS temp_result (id, name, balance, country, address, phone, comment);
