-- tsql sql:
SELECT SUSER_NAME() AS CurrentUser
FROM (
    VALUES (1)
) AS TempTable (
    TemporaryColumn
);
