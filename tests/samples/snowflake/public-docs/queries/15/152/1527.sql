-- see https://docs.snowflake.com/en/sql-reference/functions/try_to_timestamp

SELECT TRY_TO_TIMESTAMP('2018-09-15 12:30:00'), TRY_TO_TIMESTAMP('Invalid');