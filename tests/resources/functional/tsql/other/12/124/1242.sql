--Query type: DDL
CREATE TABLE Customer.CustomerTable
(
    CustomerKey INT PRIMARY KEY,
    CustomerName NVARCHAR(25) NOT NULL
);
-- REMORPH CLEANUP: DROP TABLE Customer.CustomerTable;