--Query type: DCL
DECLARE @LoginName sysname = 'NewUser';
DECLARE @CredentialName sysname = 'NewCredential';

WITH SimulatedLoginCredentials AS (
    SELECT @LoginName AS LoginName, @CredentialName AS CredentialName
)
SELECT LoginName, CredentialName
FROM SimulatedLoginCredentials;

WITH SimulatedServerPrincipals AS (
    SELECT @LoginName AS name, 'SQL_LOGIN' AS type_desc
)
SELECT name, type_desc
FROM SimulatedServerPrincipals
WHERE name = @LoginName;