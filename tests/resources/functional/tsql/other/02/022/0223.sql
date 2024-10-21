--Query type: DML
CREATE PROCEDURE demo_procedure
AS
BEGIN
    WITH temp_result AS (
        SELECT 'This is a demo procedure' AS message
    )
    SELECT *
    FROM temp_result;
END;
EXEC demo_procedure;
-- REMORPH CLEANUP: DROP PROCEDURE demo_procedure;