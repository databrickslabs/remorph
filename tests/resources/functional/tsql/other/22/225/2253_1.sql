--Query type: TCL
CREATE TABLE #SalesData
(
    SalesID INT,
    SalesDate DATE,
    ProductName VARCHAR(100),
    Quantity INT,
    Revenue DECIMAL(10, 2)
);

WITH SalesDataCTE AS
(
    SELECT *
    FROM (
        VALUES
        (
            1,
            '2022-04-01',
            'Product A',
            10,
            100.00
        ),
        (
            2,
            '2022-04-15',
            'Product B',
            20,
            200.00
        ),
        (
            3,
            '2022-04-20',
            'Product C',
            30,
            300.00
        )
    ) AS SalesData (SalesID, SalesDate, ProductName, Quantity, Revenue)
)
INSERT INTO #SalesData (SalesID, SalesDate, ProductName, Quantity, Revenue)
SELECT *
FROM SalesDataCTE;

SELECT *
FROM #SalesData;

-- REMORPH CLEANUP: DROP TABLE #SalesData;
