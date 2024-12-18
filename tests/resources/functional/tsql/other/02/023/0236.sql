-- tsql sql:
CREATE PROCEDURE demo_loop
AS
BEGIN
    WITH numbers AS (
        SELECT 1 AS i
        UNION ALL
        SELECT i + 1
        FROM numbers
        WHERE i < 5
    )
    SELECT 'Loop iteration: ' + CONVERT(VARCHAR, i) AS message
    FROM numbers
    OPTION (MAXRECURSION 0);
END;

EXEC demo_loop;
-- REMORPH CLEANUP: DROP PROCEDURE demo_loop;
