-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

--Or, query data using the WITH clause on a CSV, where schema inference is not supported
SELECT TOP 10 id, updated, confirmed, confirmed_change
FROM OPENROWSET(
 BULK 'bing_covid-19_data.csv',
 DATA_SOURCE = 'MyExternalDataSource',
 FORMAT = 'CSV',
 FIRSTROW = 2
)
WITH (
 id int,
 updated date,
 confirmed int,
 confirmed_change int
) AS filerows