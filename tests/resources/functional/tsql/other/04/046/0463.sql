-- tsql sql:
CREATE EXTERNAL DATA SOURCE MyExternalSource
WITH (
    LOCATION = 'sqlserver://MySqlServer',
    CREDENTIAL = MyCredentials
);
-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE MyExternalSource;
