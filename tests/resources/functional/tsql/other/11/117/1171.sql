--Query type: DDL
CREATE TABLE #CustomerCTE
(
    CustomerKey INT,
    EmailAddress VARCHAR(255)
);

INSERT INTO #CustomerCTE
    (
        CustomerKey,
        EmailAddress
    )
SELECT 1 AS CustomerKey, 'customer1@example.com' AS EmailAddress
UNION ALL
SELECT 2, 'customer2@example.com'
UNION ALL
SELECT 3, 'customer3@example.com';

CREATE STATISTICS CustomerStatsSampleScan ON #CustomerCTE (CustomerKey, EmailAddress) WITH SAMPLE 50 PERCENT;

SELECT * FROM #CustomerCTE;

-- REMORPH CLEANUP: DROP TABLE #CustomerCTE;
-- REMORPH CLEANUP: DROP STATISTICS #CustomerCTE.CustomerStatsSampleScan;
