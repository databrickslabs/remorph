-- see https://docs.snowflake.com/en/sql-reference/functions-table

CREATE OR REPLACE table dates_of_interest (event_date DATE);
INSERT INTO dates_of_interest (event_date) VALUES
    ('2021-06-21'::DATE),
    ('2022-06-21'::DATE);

CREATE OR REPLACE FUNCTION record_high_temperatures_for_date(d DATE)
    RETURNS TABLE (event_date DATE, city VARCHAR, temperature NUMBER)
    as
    $$
    SELECT d, 'New York', 65.0
    UNION ALL
    SELECT d, 'Los Angeles', 69.0
    $$;