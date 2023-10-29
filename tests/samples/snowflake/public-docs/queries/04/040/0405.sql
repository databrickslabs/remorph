-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for

CREATE PROCEDURE simple_for(iteration_limit INTEGER)
RETURNS INTEGER
LANGUAGE SQL
AS
$$
    DECLARE
        counter INTEGER DEFAULT 0;
    BEGIN
        FOR i IN 1 TO iteration_limit DO
            counter := counter + 1;
        END FOR;
        RETURN counter;
    END;
$$;