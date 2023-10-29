-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/if

CREATE or replace PROCEDURE example_if(flag INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
    IF (FLAG = 1) THEN
        RETURN 'one';
    ELSEIF (FLAG = 2) THEN
        RETURN 'two';
    ELSE
        RETURN 'Unexpected input.';
    END IF;
END;
$$
;