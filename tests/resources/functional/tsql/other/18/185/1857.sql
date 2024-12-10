-- tsql sql:
DECLARE @pCustomerOptions NVARCHAR(4000) = N'[1,2,3,4]';
WITH customers AS (
  SELECT 1 AS customerID, 'Customer1' AS customerName
  UNION ALL
  SELECT 2 AS customerID, 'Customer2' AS customerName
  UNION ALL
  SELECT 3 AS customerID, 'Customer3' AS customerName
  UNION ALL
  SELECT 4 AS customerID, 'Customer4' AS customerName
)
SELECT *
FROM customers
INNER JOIN OPENJSON(@pCustomerOptions) AS customerTypes
  ON customers.customerID = customerTypes.value;
-- REMORPH CLEANUP: DROP TABLE customers;
