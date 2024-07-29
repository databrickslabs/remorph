
-- snowflake sql:
select date_from_parts(2023, 10, 3), date_from_parts(2020, 4, 4);

-- databricks sql:
SELECT MAKE_DATE(2023, 10, 3), MAKE_DATE(2020, 4, 4);
