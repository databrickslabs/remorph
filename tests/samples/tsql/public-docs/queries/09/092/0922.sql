-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openrowset-transact-sql?view=sql-server-ver16

CREATE DATABASE SCOPED CREDENTIAL sampletestcred WITH IDENTITY = 'MANAGED IDENTITY';

CREATE EXTERNAL DATA SOURCE SampleSource
WITH (TYPE = BLOB_STORAGE,
LOCATION = 'https://****************.blob.core.windows.net/curriculum',
CREDENTIAL = sampletestcred