-- see https://docs.snowflake.com/en/sql-reference/functions/try_to_time

SELECT TRY_TO_TIME('12:30:00'), TRY_TO_TIME('Invalid');