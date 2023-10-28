CREATE PROCEDURE p2()
...
$$
    BEGIN TRANSACTION;
    statement C;
    COMMIT;
$$;

CREATE PROCEDURE p1()
...
$$
    BEGIN TRANSACTION;
    statement B;
    CALL p2();
    statement D;
    COMMIT;
$$;

BEGIN TRANSACTION;
statement A;
CALL p1();
statement E;
COMMIT;