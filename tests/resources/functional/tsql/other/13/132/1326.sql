-- tsql sql:
CREATE TABLE myNewTable
(
    CustomerName NVARCHAR(100),
    ProductType NVARCHAR(50),
    OrderDetails VARBINARY(max)
);
-- REMORPH CLEANUP: DROP TABLE myNewTable;
