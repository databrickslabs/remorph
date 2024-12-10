-- tsql sql:
CREATE PROCEDURE demo_procedure
AS
BEGIN
    SELECT 'Procedure called successfully' AS message;
END;
EXEC demo_procedure;
SELECT *
FROM (
    VALUES ('Procedure called successfully')
) AS demo_result (message);
-- REMORPH CLEANUP: DROP PROCEDURE demo_procedure;
