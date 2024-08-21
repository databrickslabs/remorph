
-- snowflake sql:
select TIMESTAMP_FROM_PARTS(2023, 10, 3, 14, 10, 45),
                timestamp_from_parts(2020, 4, 4, 4, 5, 6);

-- databricks sql:
SELECT MAKE_TIMESTAMP(2023, 10, 3, 14, 10, 45), MAKE_TIMESTAMP(2020, 4, 4, 4, 5, 6);
