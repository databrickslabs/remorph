EXECUTE IMMEDIATE $$
    DECLARE
        i INTEGER;
        j INTEGER;
    BEGIN
        i := 1;
        j := 1;
        WHILE (i <= 4) DO
            WHILE (j <= 4) DO
                -- Exit when j is 3, even if i is still 1.
                IF (j = 3) THEN
                     BREAK outer_loop;
                END IF;
                j := j + 1;
            END WHILE inner_loop;
            i := i + 1;
        END WHILE outer_loop;
        -- Execution resumes here after the BREAK executes.
        RETURN i;
    END;
$$;