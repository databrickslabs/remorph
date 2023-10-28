EXECUTE IMMEDIATE $$
    DECLARE
        profit number(38, 2) DEFAULT 0.0;
    BEGIN
        LET cost number(38, 2) := 100.0;
        LET revenue number(38, 2) DEFAULT 110.0;

        profit := revenue - cost;
        RETURN profit;
    END;
$$
;