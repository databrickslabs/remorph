-- tsql sql:
EXECUTE ('CREATE TABLE Customer.OrdersTable (OrderID INT, OrderName VARCHAR(10));') AS USER = 'User2'; -- REMORPH CLEANUP: DROP TABLE Customer.OrdersTable; -- REMORPH CLEANUP: DROP USER User2;
