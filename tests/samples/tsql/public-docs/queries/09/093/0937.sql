-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

CREATE DATABASE [<mydatabase>];
GO

USE [<mydatabase>];
GO

CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<strong password>';

CREATE DATABASE SCOPED CREDENTIAL [WorkspaceIdentity] WITH IDENTITY = 'Managed Identity';
GO

CREATE EXTERNAL FILE FORMAT [ParquetFF] WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);
GO

CREATE EXTERNAL DATA SOURCE [SynapseSQLwriteable] WITH (
    LOCATION = 'https://<mystoageaccount>.dfs.core.windows.net/<mycontainer>/<mybaseoutputfolderpath>',
    CREDENTIAL = [WorkspaceIdentity]
);
GO

CREATE EXTERNAL TABLE [dbo].[<myexternaltable>] WITH (
        LOCATION = '<myoutputsubfolder>/',
        DATA_SOURCE = [SynapseSQLwriteable],
        FILE_FORMAT = [ParquetFF]
) AS
SELECT * FROM [<myview>];
GO