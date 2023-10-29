-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/copy-into-transact-sql?view=azure-sqldw-latest

COPY INTO [myCOPYDemoTable]
FROM 'https://myaccount.blob.core.windows.net/customerdatasets/folder1/lineitem.parquet'
WITH (
    FILE_TYPE = 'Parquet',
    CREDENTIAL = ( IDENTITY = 'Shared Access Signature',  SECRET='<key>'),
    AUTO_CREATE_TABLE = 'ON'
)