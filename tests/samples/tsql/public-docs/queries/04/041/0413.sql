-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

--Create external data source pointing to the file path, and referencing database-scoped credential:
CREATE EXTERNAL DATA SOURCE MyPrivateExternalDataSource
WITH (
    LOCATION = 'abs://public@pandemicdatalake.blob.core.windows.net/curated/covid-19/bing_covid-19_data/latest'
        CREDENTIAL = [MyCredential]
)
GO