-- tsql sql:
CREATE TABLE #SupplierTable
(
    SupplierKey INT,
    AddressLine1 VARCHAR(50)
);

INSERT INTO #SupplierTable
(
    SupplierKey,
    AddressLine1
)
VALUES
(
    1,
    '123 Main St'
),
(
    2,
    '456 Elm St'
);

CREATE STATISTICS SupplierStatsFullScan
ON #SupplierTable
(
    SupplierKey,
    AddressLine1
)
WITH FULLSCAN;

SELECT *
FROM #SupplierTable;

-- REMORPH CLEANUP: DROP TABLE #SupplierTable;

-- REMORPH CLEANUP: DROP STATISTICS #SupplierTable.SupplierStatsFullScan;
