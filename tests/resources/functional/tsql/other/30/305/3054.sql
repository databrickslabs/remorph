--Query type: DML
SELECT TOP 0 *
INTO #temp
FROM (
    VALUES (
        1, 101, '2022-01-01', 100.00
        ), (
        2, 102, '2022-01-02', 200.00
        ), (
        3, 103, '2022-01-03', 300.00
        )
    ) AS sales (
        sale_id, product_id, sale_date, sale_amount
    );
UPDATE STATISTICS #temp (sale_id) WITH NORECOMPUTE;
SELECT *
FROM #temp;
-- REMORPH CLEANUP: DROP TABLE #temp;