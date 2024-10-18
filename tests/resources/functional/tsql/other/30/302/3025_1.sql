--Query type: DDL
IF EXISTS (SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NewTable')
    DROP TABLE NewTable;

CREATE TABLE NewTable
(
    CustomerID INT,
    OrderID INT
);

INSERT INTO NewTable (CustomerID, OrderID)
SELECT CustomerID, OrderID
FROM (
    VALUES (1, 1),
           (2, 2),
           (3, 3)
) AS NewValues (CustomerID, OrderID);

SELECT *
FROM NewTable;

-- REMORPH CLEANUP: DROP TABLE NewTable;