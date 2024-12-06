-- tsql sql:
CREATE EXTERNAL DATA SOURCE MyNewExternalDataSource
WITH (
    LOCATION = 'abs://public@pandemicdatalake.blob.core.windows.net/curated/covid-19/bing_covid-19_data/archive',
    CREDENTIAL = MyNewCredential
);
-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE MyNewExternalDataSource;
