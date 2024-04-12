
-- snowflake sql:
select dateadd('day', 3, '2020-02-03'::date);

-- databricks sql:
SELECT DATEADD(day, 3, CAST('2020-02-03' AS DATE));
