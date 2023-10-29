-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE DATABASE SCOPED CREDENTIAL SQLServerCredentials
WITH IDENTITY = 'username', SECRET = 'password';