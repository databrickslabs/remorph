-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for

CREATE PROCEDURE reverse_loop(iteration_limit INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        values_of_i VARCHAR DEFAULT '';
    BEGIN
        FOR i IN REVERSE 1 TO iteration_limit DO
            values_of_i := values_of_i || ' ' || i::varchar;
        END FOR;
        RETURN values_of_i;
    END;
$$;