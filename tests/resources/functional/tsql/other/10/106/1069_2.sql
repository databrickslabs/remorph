--Query type: DDL
CREATE TABLE Customer (custkey int, name varchar(25), address varchar(40));
INSERT INTO Customer (custkey, name, address)
SELECT *
FROM (
    VALUES (1, 'Customer#000000001', '1313 13th St.'),
    (2, 'Customer#000000002', '123 Main St.')
) AS Customer(custkey, name, address);
SELECT *
FROM Customer;
-- REMORPH CLEANUP: DROP TABLE Customer;