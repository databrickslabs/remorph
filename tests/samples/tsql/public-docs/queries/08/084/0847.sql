-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/copy-into-transact-sql?view=azure-sqldw-latest

COPY INTO t1
FROM
'https://myaccount.blob.core.windows.net/myblobcontainer/folder0/*.txt',
    'https://myaccount.blob.core.windows.net/myblobcontainer/folder1'
WITH (
    FILE_TYPE = 'CSV',
    CREDENTIAL=(IDENTITY= '<client_id>@<OAuth_2.0_Token_EndPoint>',SECRET='<key>'),
    FIELDTERMINATOR = '|'
)