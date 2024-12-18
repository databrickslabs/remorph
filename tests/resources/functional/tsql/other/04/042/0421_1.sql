-- tsql sql:
CREATE VIEW dbo.all_customer_view
WITH SCHEMABINDING
AS
    SELECT customerID, customerName
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS CUSTOMER1 (customerID, customerName)
    UNION ALL
    SELECT customerID, customerName
    FROM (
        VALUES (3, 'Customer3'),
               (4, 'Customer4')
    ) AS CUSTOMER2 (customerID, customerName)
    UNION ALL
    SELECT customerID, customerName
    FROM (
        VALUES (5, 'Customer5'),
               (6, 'Customer6')
    ) AS CUSTOMER3 (customerID, customerName)
    UNION ALL
    SELECT customerID, customerName
    FROM (
        VALUES (7, 'Customer7'),
               (8, 'Customer8')
    ) AS CUSTOMER4 (customerID, customerName);
-- REMORPH CLEANUP: DROP VIEW dbo.all_customer_view;
