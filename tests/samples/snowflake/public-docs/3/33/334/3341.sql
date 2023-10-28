create procedure ...
    as
    $$
        ...
        statement1;

        BEGIN TRANSACTION;
        statement2;
        COMMIT;

        statement3;
        ...

    $$;