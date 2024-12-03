--Query type: DDL
CREATE TYPE CustomerTableType AS TABLE (
    CustomerName VARCHAR(50),
    Address VARCHAR(100),
    Phone VARCHAR(20)
);

WITH CustomerCTE AS (
    SELECT 'John Doe' AS CustomerName, '123 Main St' AS Address, '123-456-7890' AS Phone
    UNION ALL
    SELECT 'Jane Doe' AS CustomerName, '456 Elm St' AS Address, '987-654-3210' AS Phone
)
SELECT * FROM CustomerCTE;
-- REMORPH CLEANUP: DROP TYPE CustomerTableType;
