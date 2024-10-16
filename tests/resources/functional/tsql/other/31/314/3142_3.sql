--Query type: DDL
IF OBJECT_ID('dbo.CustomerTwo', 'U') IS NOT NULL
    DROP TABLE dbo.CustomerTwo;

WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS Customer(c_custkey, c_name, c_address)
)
SELECT *
FROM CustomerCTE;
-- REMORPH CLEANUP: DROP TABLE dbo.CustomerTwo;