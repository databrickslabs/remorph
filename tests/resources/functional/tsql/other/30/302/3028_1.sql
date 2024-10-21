--Query type: DCL
SETUSER;
WITH temp AS (
    SELECT 'Current User' AS [User]
)
SELECT * FROM temp;