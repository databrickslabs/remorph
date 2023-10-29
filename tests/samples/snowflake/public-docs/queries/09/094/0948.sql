-- see https://docs.snowflake.com/en/sql-reference/functions/add_months

SELECT ADD_MONTHS('2016-05-15'::timestamp_ntz, 2) AS RESULT;