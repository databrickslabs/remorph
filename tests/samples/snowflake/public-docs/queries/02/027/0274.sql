-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for

CREATE OR REPLACE PROCEDURE for_loop_over_cursor()
RETURNS FLOAT
LANGUAGE SQL
AS
$$
DECLARE
    total_price FLOAT;
    c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
    total_price := 0.0;
    OPEN c1;
    FOR rec IN c1 DO
        total_price := total_price + rec.price;
    END FOR;
    CLOSE c1;
    RETURN total_price;
END;
$$
;