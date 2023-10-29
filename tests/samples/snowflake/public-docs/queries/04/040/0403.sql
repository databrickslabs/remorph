-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/while

CREATE PROCEDURE power_of_2()
RETURNS NUMBER(8, 0)
LANGUAGE SQL
AS
$$
DECLARE
    counter NUMBER(8, 0);      -- Loop counter.
    power_of_2 NUMBER(8, 0);   -- Stores the most recent power of 2 that we calculated.
BEGIN
    counter := 1;
    power_of_2 := 1;
    WHILE (counter <= 8) DO
        power_of_2 := power_of_2 * 2;
        counter := counter + 1;
    END WHILE;
    RETURN power_of_2;
END;
$$
;