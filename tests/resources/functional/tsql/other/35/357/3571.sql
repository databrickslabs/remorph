--Query type: DCL
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'mystrongpassword123';

WITH temp_result AS (
    SELECT 1 AS id
)

SELECT * FROM temp_result;
