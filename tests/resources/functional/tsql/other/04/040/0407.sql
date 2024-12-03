--Query type: DDL
CREATE TABLE #MyOrderTable
(
    OrderKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    OrderDateKey INT NOT NULL,
    TotalPrice DECIMAL(10, 2) NOT NULL
);

INSERT INTO #MyOrderTable
(
    OrderKey,
    CustomerKey,
    OrderDateKey,
    TotalPrice
)
SELECT *
FROM (
    VALUES (1, 1, 1, 10.00)
) AS MyOrderTable
(
    OrderKey,
    CustomerKey,
    OrderDateKey,
    TotalPrice
);

CREATE CLUSTERED INDEX IDX_CL_MyOrderTable
ON #MyOrderTable (OrderKey);

SELECT *
FROM #MyOrderTable;

-- REMORPH CLEANUP: DROP TABLE #MyOrderTable;
-- REMORPH CLEANUP: DROP INDEX IDX_CL_MyOrderTable ON #MyOrderTable;
