CREATE PROCEDURE my_procedure()
...
AS
$$
    statement X;
    statement Y;
$$;

BEGIN TRANSACTION;
statement W;
CALL my_procedure();
statement Z;
COMMIT;