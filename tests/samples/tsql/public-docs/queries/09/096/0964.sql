-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE EXTERNAL DATA SOURCE POSTGRES1
WITH
(
 LOCATION = 'odbc://POSTGRES1.domain:5432'
,CONNECTION_OPTIONS = 'Driver={PostgreSQL Unicode(x64)};'
,CREDENTIAL = postgres_credential
)