-- tsql sql:
DECLARE @var3 VARCHAR(30);
SELECT @var3 = 'Customer Name';
SELECT @var3 = (
    SELECT [Name]
    FROM (
        VALUES (1, 'John'),
               (2, 'Jane')
    ) AS CustomerTable(CustomerID, Name)
    WHERE CustomerID = 1
);
SELECT @var3 AS 'Customer Name';
-- REMORPH CLEANUP: DROP TABLE CustomerTable;
