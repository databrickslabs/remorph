-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

-- External File Format for PARQUET
CREATE EXTERNAL FILE FORMAT ParquetFileFormat
    WITH (FORMAT_TYPE = PARQUET);
GO

CREATE EXTERNAL TABLE Delta_to_Parquet
    WITH (
            LOCATION = '/backup/sales.parquet',
            DATA_SOURCE = s3_parquet,
            FILE_FORMAT = ParquetFileFormat
            ) AS

SELECT *
FROM OPENROWSET(BULK '/delta/sales_fy22/', FORMAT = 'DELTA', DATA_SOURCE = 's3_delta') AS [r];
GO