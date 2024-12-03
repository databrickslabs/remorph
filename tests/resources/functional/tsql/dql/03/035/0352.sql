--Query type: DQL
WITH EmployeeCTE AS ( SELECT CustomerKey, LastName FROM ( VALUES (1, 'Smith'), (2, 'Johnson'), (3, 'Williams') ) AS Customer (LastName, CustomerKey) ) SELECT CustomerKey, LastName FROM EmployeeCTE WHERE LastName LIKE ('%Smi%');
