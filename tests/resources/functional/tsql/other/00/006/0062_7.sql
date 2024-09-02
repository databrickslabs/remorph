--Query type: DDL
CREATE VIEW customer_view
AS
SELECT c_custkey, c_name, c_address, c_phone, c_acctbal
FROM (
    VALUES (1, 'Customer 1', '123 Main St', '123-456-7890', 100.00),
    (2, 'Customer 2', '456 Elm St', '987-654-3210', 200.00),
    (3, 'Customer 3', '789 Oak St', '555-123-4567', 300.00)
) AS customer_data (c_custkey, c_name, c_address, c_phone, c_acctbal);
-- REMORPH CLEANUP: DROP VIEW customer_view;