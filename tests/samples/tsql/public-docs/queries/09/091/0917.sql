-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE DATABASE SCOPED CREDENTIAL [OracleProxyCredential]
WITH IDENTITY = 'oracle_username', SECRET = 'oracle_password';

CREATE EXTERNAL DATA SOURCE [OracleSalesSrvr]
WITH (LOCATION = 'oracle://145.145.145.145:1521',
CONNECTION_OPTIONS = 'ImpersonateUser=%CURRENT_USER',
CREDENTIAL = [OracleProxyCredential]);