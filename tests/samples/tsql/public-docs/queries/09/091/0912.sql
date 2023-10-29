-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-transact-sql?view=sql-server-ver16

CREATE DATABASE SCOPED CREDENTIAL MyCredential
WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
SECRET = '<KEY>' ; --Removing leading '?'
GO