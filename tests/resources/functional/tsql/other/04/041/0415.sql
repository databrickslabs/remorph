--Query type: DDL
WITH Customer AS ( SELECT CUSTKEY, EMAIL FROM ( VALUES (1, 'email1'), (2, 'email2') ) AS Customer(CUSTKEY, EMAIL) ) SELECT * FROM Customer;