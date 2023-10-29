-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/raise

CREATE PROCEDURE thrower()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        MY_EXCEPTION EXCEPTION;
    BEGIN
        RAISE MY_EXCEPTION;
    END;
$$
;