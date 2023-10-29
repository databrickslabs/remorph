-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

--Create a database scoped credential using SAS Token
CREATE DATABASE SCOPED CREDENTIAL datalakegen2
WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
SECRET = '<DataLakeGen2_SAS_Token>';
GO
CREATE EXTERNAL DATA SOURCE data_lake_gen2_dfs
WITH
(
LOCATION = 'adls://<container>@<storage_account>.dfs.core.windows.net'
,CREDENTIAL = datalakegen2
)