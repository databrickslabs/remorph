--Query type: DDL
WITH CustomerUSA_CTE AS (
    SELECT *
    FROM (
        VALUES (1, 'John', 'Doe'),
               (2, 'Jane', 'Doe')
    ) AS CustomerUSA (Id, FirstName, LastName)
)
SELECT *
INTO dbo.Customer
FROM CustomerUSA_CTE;
-- REMORPH CLEANUP: DROP TABLE dbo.Customer;
