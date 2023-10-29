-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-file-format-transact-sql?view=sql-server-ver16

CREATE EXTERNAL FILE FORMAT jsonFileFormat
WITH (
    FORMAT_TYPE = JSON,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);