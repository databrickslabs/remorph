
-- snowflake sql:
select datediff('day', '2020-02-03'::timestamp, '2023-10-26'::timestamp);

-- databricks sql:
SELECT DATEDIFF(day, CAST('2020-02-03' AS TIMESTAMP), CAST('2023-10-26' AS TIMESTAMP));
