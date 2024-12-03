--Query type: DCL
EXECUTE AS USER = 'Luigi';
WITH temp_result AS (
    SELECT SUSER_NAME() AS username
)
SELECT *
FROM temp_result;
REVERT;
