-- tsql sql:
CREATE LOGIN [newuser@contoso.com] FROM EXTERNAL PROVIDER;
WITH tempResult AS (
    SELECT 'example' AS data
)
SELECT * FROM tempResult;
