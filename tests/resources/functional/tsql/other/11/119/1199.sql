-- tsql sql:
CREATE TABLE NewTable
(
    OrderKey int PRIMARY KEY,
    OrderStatus rowversion,
    OrderTotal decimal(10, 2),
    OrderDate date
);
-- REMORPH CLEANUP: DROP TABLE NewTable;
