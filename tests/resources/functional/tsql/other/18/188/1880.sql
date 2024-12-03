--Query type: DML
DECLARE @stringVar NVARCHAR(100);
SET @stringVar = N'WITH logins AS (
    SELECT ''login1'' AS name
    UNION
    SELECT ''login2''
    UNION
    SELECT ''login3''
)
SELECT name
FROM logins';
EXEC (@stringVar);
