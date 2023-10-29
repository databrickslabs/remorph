-- see https://docs.snowflake.com/en/sql-reference/functions/try_to_double

SELECT TRY_TO_DOUBLE('3.1415926'), TRY_TO_DOUBLE('Invalid');