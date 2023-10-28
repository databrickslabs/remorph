EXECUTE IMMEDIATE $$
    DECLARE
        RESULT VARCHAR;
        e1 EXCEPTION (-20001, 'Outer exception e1');

    BEGIN
        RESULT := 'No error so far (but there will be).';

        DECLARE
            e1 EXCEPTION (-20101, 'Inner exception e1');
        BEGIN
            RAISE e1;
        EXCEPTION
            WHEN e1 THEN
                RESULT := 'Inner exception raised.';
                RETURN RESULT;
        END;

        RETURN RESULT;

    EXCEPTION
        WHEN e1 THEN
            RESULT := 'Outer exception raised.';
            RETURN RESULT;

    END;
$$
;