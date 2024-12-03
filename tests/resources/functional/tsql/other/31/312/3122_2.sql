--Query type: DCL
CREATE TABLE #Customer (customer_id INT, customer_name VARCHAR(50));
INSERT INTO #Customer (customer_id, customer_name)
VALUES (1, 'customer1'), (2, 'customer2');
DBCC CHECKCONSTRAINTS ('#Customer');
SELECT * FROM #Customer;
-- REMORPH CLEANUP: DROP TABLE #Customer;
