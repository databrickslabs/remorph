
-- source:
select timestampDIFF(month, '2021-01-01'::timestamp, '2021-02-28'::timestamp);

-- databricks_sql:
SELECT DATEDIFF(month, CAST('2021-01-01' AS TIMESTAMP), CAST('2021-02-28' AS TIMESTAMP));
