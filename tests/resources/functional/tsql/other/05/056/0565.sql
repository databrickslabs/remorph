--Query type: DDL
ALTER DATABASE db1
    MODIFY (SERVICE_OBJECTIVE = ELASTIC_POOL (name = pool1));

SELECT
    CASE
        WHEN SUM(CASE WHEN region = 'North' THEN sales ELSE 0 END) > SUM(CASE WHEN region = 'South' THEN sales ELSE 0 END)
            THEN 'North has more total sales'
        WHEN SUM(CASE WHEN region = 'North' THEN sales ELSE 0 END) < SUM(CASE WHEN region = 'South' THEN sales ELSE 0 END)
            THEN 'South has more total sales'
        ELSE 'North and South have the same total sales'
    END AS result
FROM (
    VALUES ('North', 500), ('North', 600), ('South', 200), ('South', 700)
) AS sales_data (region, sales);