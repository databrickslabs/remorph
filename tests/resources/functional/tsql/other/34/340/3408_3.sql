--Query type: TCL
BEGIN TRANSACTION;
SELECT *
FROM (
    VALUES (
        (1, 2),
        (3, 4)
    )
) AS temp_table (a, b);
COMMIT TRANSACTION;