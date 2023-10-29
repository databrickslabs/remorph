-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for

CREATE PROCEDURE p(iteration_limit INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        counter INTEGER DEFAULT 0;
        i INTEGER DEFAULT -999;
        return_value VARCHAR DEFAULT '';
    BEGIN
        FOR i IN 1 TO iteration_limit DO
            counter := counter + 1;
        END FOR;
        return_value := 'counter: ' || counter::varchar || '\n';
        return_value := return_value || 'i: ' || i::VARCHAR;
        RETURN return_value;
    END;
$$;