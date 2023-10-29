-- see https://docs.snowflake.com/en/sql-reference/functions-table

SELECT
        doi.event_date as "Date", 
        record_temperatures.city,
        record_temperatures.temperature
    FROM dates_of_interest AS doi,
         TABLE(record_high_temperatures_for_date(doi.event_date)) AS record_temperatures
      ORDER BY doi.event_date, city;