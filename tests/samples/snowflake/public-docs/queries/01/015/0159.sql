-- see https://docs.snowflake.com/en/sql-reference/functions/convert_timezone

ALTER SESSION UNSET timestamp_output_format;

-- Show the current "wallclock" time in different time zones

SELECT
    CURRENT_TIMESTAMP() AS now_in_la,
    CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
    CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
    CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo;
