-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/raise

DECLARE
        MY_EXCEPTION EXCEPTION (-20002, 'Raised MY_EXCEPTION.');