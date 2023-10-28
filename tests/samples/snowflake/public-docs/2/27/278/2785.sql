CREATE TABLE dummy_data (ID INTEGER);

CREATE PROCEDURE break_out_of_loop()
RETURNS INTEGER
LANGUAGE SQL
AS
$$
    DECLARE
        counter INTEGER;
    BEGIN
        counter := 0;
        LOOP
            counter := counter + 1;
            IF (counter > 5) THEN
                BREAK;
            END IF;
            INSERT INTO dummy_data (ID) VALUES (:counter);
        END LOOP;
        RETURN counter;
    END;
$$
;