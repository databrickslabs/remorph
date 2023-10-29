-- see https://docs.snowflake.com/en/sql-reference/data-type-conversion

SELECT date_column
    FROM log_table
    WHERE date_column >= '2022-04-01'::DATE;