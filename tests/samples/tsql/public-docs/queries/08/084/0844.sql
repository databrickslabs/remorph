-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/copy-into-transact-sql?view=azure-sqldw-latest

COPY INTO dbo.[lineitem]
FROM 'https://unsecureaccount.blob.core.windows.net/customerdatasets/folder1/lineitem.csv'