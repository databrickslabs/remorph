-- see https://docs.snowflake.com/en/sql-reference/functions/convert_timezone

ALTER SESSION UNSET timestamp_output_format;

-- Convert TIMESTAMP_TZ to a different time zone and include the time zone in the result

SELECT CONVERT_TIMEZONE('America/Los_Angeles', '2018-04-05 12:00:00 +02:00') AS time_in_la;
