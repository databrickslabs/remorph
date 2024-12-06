-- tsql sql:
WITH DimCustomer_old AS ( SELECT * FROM ( VALUES (1, 'Customer1'), (2, 'Customer2') ) AS T (CustomerKey, CustomerName) ) SELECT * FROM DimCustomer_old;
