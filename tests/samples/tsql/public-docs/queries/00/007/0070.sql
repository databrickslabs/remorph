-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

-- Credential to access the S3-compatible object storage
CREATE DATABASE SCOPED CREDENTIAL s3_dsc
    WITH IDENTITY = 'S3 Access Key',
        SECRET = '<accesskeyid>:<secretkeyid>'
GO

-- S3-compatible object storage data source
CREATE EXTERNAL DATA SOURCE s3_eds
    WITH (
            LOCATION = 's3://<ip>:<port>',
            CREDENTIAL = s3_dsc
            )

-- External File Format for PARQUET
CREATE EXTERNAL FILE FORMAT ParquetFileFormat
    WITH (FORMAT_TYPE = PARQUET);
GO

CREATE EXTERNAL TABLE ext_sales
    WITH (
            LOCATION = '/cetas/sales.parquet',
            DATA_SOURCE = s3_eds,
            FILE_FORMAT = ParquetFileFormat
            ) AS

SELECT *
FROM AdventureWorks2022.[Sales].[SalesOrderDetail];
GO