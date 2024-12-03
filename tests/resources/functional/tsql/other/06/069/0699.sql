--Query type: DML
DECLARE customer_cursor CURSOR FOR SELECT c_custkey, c_name, c_address FROM (VALUES (1, 'Customer#1', '123 Main St'), (2, 'Customer#2', '456 Elm St')) AS customers(c_custkey, c_name, c_address);
OPEN customer_cursor;
FETCH NEXT FROM customer_cursor;
CLOSE customer_cursor;
DEALLOCATE customer_cursor;
-- REMORPH CLEANUP: DROP TABLE customers;
