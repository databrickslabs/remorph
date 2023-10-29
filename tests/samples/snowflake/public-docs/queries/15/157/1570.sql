-- see https://docs.snowflake.com/en/sql-reference/functions-table

SELECT city_name, temperature
    FROM TABLE(record_high_temperatures_for_date('2021-06-27'::DATE))
    ORDER BY city_name;