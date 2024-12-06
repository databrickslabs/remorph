-- tsql sql:
IF EXISTS (SELECT 1 FROM sys.database_scoped_credentials WHERE name = 'NewAppCred')
    DROP DATABASE SCOPED CREDENTIAL NewAppCred;

CREATE DATABASE SCOPED CREDENTIAL NewAppCred
    WITH IDENTITY = 'NewRettigB',
         SECRET = 'new_sdrlk8$40-dksli87nNN8';

SELECT *
FROM sys.database_scoped_credentials
WHERE name = 'NewAppCred';

-- REMORPH CLEANUP: DROP DATABASE SCOPED CREDENTIAL NewAppCred;
