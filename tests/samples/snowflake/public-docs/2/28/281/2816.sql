EXECUTE IMMEDIATE $$
    DECLARE
        RESULT VARCHAR;
        EXCEPTION_1 EXCEPTION (-20001, 'I caught the expected exception.');
        EXCEPTION_2 EXCEPTION (-20002, 'Not the expected exception!');
    BEGIN
        RESULT := 'If you see this, I did not catch any exception.';
        IF (TRUE) THEN
            RAISE EXCEPTION_1;
        END IF;
        RETURN RESULT;
    EXCEPTION
        WHEN EXCEPTION_2 THEN
            RETURN SQLERRM;
        WHEN EXCEPTION_1 THEN
            RETURN SQLERRM;
    END;
$$
;