-- tsql sql:
WITH Customer AS ( SELECT * FROM ( VALUES (1, 'Customer#000000001'), (2, 'Customer#000000002') ) AS Customer (C_CustomerKey, C_Name) ) SELECT * FROM Customer;
