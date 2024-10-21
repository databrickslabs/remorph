--Query type: DML
CREATE PROCEDURE test_procedure
AS
BEGIN
    WITH temp_result AS (
        SELECT 'Hello World!' AS message
    )
    SELECT *
    FROM temp_result;
END;
EXEC test_procedure;