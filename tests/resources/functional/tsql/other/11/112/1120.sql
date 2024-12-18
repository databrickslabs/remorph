-- tsql sql:
CREATE TABLE #SalesRoute
(
    SERVICE_NAME nvarchar(255),
    BROKER_INSTANCE uniqueidentifier,
    ADDRESS nvarchar(255)
);

INSERT INTO #SalesRoute
(
    SERVICE_NAME,
    BROKER_INSTANCE,
    ADDRESS
)
VALUES
(
    '//TPC-H.com/Sales',
    '12345678-1234-1234-1234-123456789012',
    'TCP://10.10.10.1:5678'
);

SELECT *
FROM #SalesRoute;

-- REMORPH CLEANUP: DROP TABLE #SalesRoute;
