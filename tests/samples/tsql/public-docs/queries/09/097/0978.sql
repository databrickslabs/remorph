-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE EXTERNAL DATA SOURCE [external_data_source_name]
WITH (
LOCATION = N'oracle://XE', 
CREDENTIAL = [OracleCredentialTest], 
CONNECTION_OPTIONS = N'TNSNamesFile=C:\Temp\tnsnames.ora;ServerName=XE'
)
GO