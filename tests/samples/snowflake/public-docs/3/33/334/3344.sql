CREATE PROCEDURE p1()
...
$$
    begin transaction;
    statement C;
    statement D;
    commit;

    begin transaction;
    statement E;
    statement F;
    commit;
$$;