--Query type: DDL
CREATE DATABASE MyNewLedgerDB (EDITION = 'GeneralPurpose') WITH (LEDGER = ON);
WITH MyCTE AS (
    SELECT 1 AS Column1
)
SELECT * FROM MyCTE;
