--Query type: DML
CREATE PROCEDURE p2
AS
BEGIN
    WITH temp_result AS (
        SELECT 'Hello, World!' AS message
    )
    SELECT *
    FROM temp_result;
END;
EXEC p2;
