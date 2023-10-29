-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openrowset-transact-sql?view=sql-server-ver16

SELECT * FROM OPENROWSET(
BULK 'Test - Copy.csv',
DATA_SOURCE = 'SampleSource',
SINGLE_CLOB
) as test