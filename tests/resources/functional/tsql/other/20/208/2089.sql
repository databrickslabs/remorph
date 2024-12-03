--Query type: DCL
EXECUTE AS USER = 'CustomApp';
WITH temp_result AS (
    SELECT CURRENT_USER AS CurrentUser
)
SELECT *
FROM temp_result;
REVERT;
