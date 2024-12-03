--Query type: DDL
CREATE TABLE #CustomerTable
(
    CustomerKey INT,
    EmailAddress VARCHAR(255)
);

INSERT INTO #CustomerTable
(
    CustomerKey,
    EmailAddress
)
SELECT
    CustomerKey,
    EmailAddress
FROM
(
    VALUES
    (
        1,
        'customer1@example.com'
    ),
    (
        2,
        'customer2@example.com'
    )
) AS CustomerTable
(
    CustomerKey,
    EmailAddress
);

CREATE STATISTICS CustomerStats2
ON #CustomerTable
(
    CustomerKey,
    EmailAddress
)
WITH FULLSCAN;

SELECT *
FROM #CustomerTable;

-- REMORPH CLEANUP: DROP TABLE #CustomerTable;
-- REMORPH CLEANUP: DROP STATISTICS #CustomerTable.CustomerStats2;
