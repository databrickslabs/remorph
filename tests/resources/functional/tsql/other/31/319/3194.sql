--Query type: DCL
CREATE DATABASE TPC_H;
CREATE USER SalesManager;
GRANT CONTROL ON DATABASE::TPC_H TO SalesManager;
WITH SalesCTE AS (
    SELECT *
    FROM (
        VALUES ('Sales1', 100), ('Sales2', 200)
    ) AS Sales(SalesName, SalesAmount)
)
SELECT *
FROM SalesCTE;
-- REMORPH CLEANUP: DROP DATABASE TPC_H;
-- REMORPH CLEANUP: DROP USER SalesManager;