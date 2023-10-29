-- see https://docs.snowflake.com/en/sql-reference/functions/convert_timezone

ALTER SESSION SET timestamp_output_format = 'YYYY-MM-DD HH24:MI:SS';

-- Convert a "wallclock" time in Los Angeles to the matching "wallclock" time in New York

SELECT CONVERT_TIMEZONE('America/Los_Angeles', 'America/New_York', '2019-01-01 14:00:00'::timestamp_ntz) AS conv;


-- Convert a "wallclock" time in Warsaw to the matching "wallclock" time in UTC

SELECT CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00'::timestamp_ntz) AS conv;
