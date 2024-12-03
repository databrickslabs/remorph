--Query type: DDL
CREATE TABLE Orders
(
    OrderKey INT PRIMARY KEY,
    CustomerKey INT NULL,
    FOREIGN KEY (CustomerKey) REFERENCES Customer(CustomerKey)
);
-- REMORPH CLEANUP: DROP TABLE Orders;
