
-- source:
select dateadd('day', 3, '2020-02-03'::date);

-- databricks_sql:
SELECT DATEADD(day, 3, CAST('2020-02-03' AS DATE));
