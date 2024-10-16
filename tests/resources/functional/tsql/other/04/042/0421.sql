--Query type: DDL
CREATE TABLE CUSTOMER (
    customerID INT PRIMARY KEY
    CHECK (customerID BETWEEN 1 AND 600),
    customerName CHAR(50)
);
INSERT INTO CUSTOMER (customerID, customerName)
VALUES (1, 'Customer 1'),
       (2, 'Customer 2'),
       (600, 'Customer 600');
SELECT *
FROM CUSTOMER;
-- REMORPH CLEANUP: DROP TABLE CUSTOMER;