EXECUTE IMMEDIATE $$
    DECLARE
        e1 EXCEPTION (-20001, 'Exception e1');

    BEGIN
        -- Inner block.
        DECLARE
            e2 EXCEPTION (-20002, 'Exception e2');
            selector BOOLEAN DEFAULT TRUE;
        BEGIN
            IF (selector) THEN
                RAISE e1;
            ELSE
                RAISE e2;
            END IF;
        END;

    EXCEPTION
        WHEN e1 THEN
            BEGIN
                RETURN SQLERRM || ' caught in outer block.';
            END;

    END;
$$
;