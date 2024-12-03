--Query type: DML
DECLARE @error_message nvarchar(255);

WITH temp_result AS (
    SELECT 'This is a custom error message.' AS error_message
)

SELECT @error_message = error_message
FROM temp_result;

THROW 50000, @error_message, 1;
