
-- source:
select timestampadd(year, -3, '2023-02-03 01:02'::timestamp);

-- databricks_sql:
SELECT DATEADD(year, -3, CAST('2023-02-03 01:02' AS TIMESTAMP));
