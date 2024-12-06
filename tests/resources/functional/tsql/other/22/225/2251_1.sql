-- tsql sql:
DECLARE @DimCustomer TABLE (CustomerName VARCHAR(50), CustomerID INT);
INSERT INTO @DimCustomer (CustomerName, CustomerID)
VALUES ('Customer1', 1);
SELECT *
FROM @DimCustomer AS DimCustomer_Renamed;
-- REMORPH CLEANUP: DROP TABLE @DimCustomer;
