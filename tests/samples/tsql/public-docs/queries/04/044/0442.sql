-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

--Query data with OPENROWSET, relying on schema inference.
SELECT TOP 10 *
FROM OPENROWSET(
 BULK 'bing_covid-19_data.parquet',
 DATA_SOURCE = 'MyExternalDataSource',
 FORMAT = 'parquet'
) AS filerows