-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-file-format-transact-sql?view=sql-server-ver16

CREATE EXTERNAL FILE FORMAT textdelimited1
WITH (
    FORMAT_TYPE = DELIMITEDTEXT,
    FORMAT_OPTIONS (
        FIELD_TERMINATOR = '|',
        DATE_FORMAT = 'MM/dd/yyyy' ),
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.GzipCodec'
);