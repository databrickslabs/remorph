--Query type: DDL
CREATE TABLE #SalesData
(
    region_key INT,
    sales_amount DECIMAL(10, 2),
    sales_date DATE
);

WITH SalesData AS
(
    SELECT region_key, sales_amount, sales_date
    FROM (
        VALUES (1, 500.0, '2020-03-01'),
               (2, 750.0, '2020-04-15'),
               (3, 300.0, '2020-05-01')
    ) AS SalesData(region_key, sales_amount, sales_date)
)
INSERT INTO #SalesData (region_key, sales_amount, sales_date)
SELECT region_key, sales_amount, sales_date
FROM SalesData;

SELECT *
FROM #SalesData;

-- REMORPH CLEANUP: DROP TABLE #SalesData;