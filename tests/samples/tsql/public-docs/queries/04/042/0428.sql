-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

--Example 1: Creating an external table into a single parquet file on the storage, selecting from SalesOrderHeader table for orders older than 1-Jan-2014:
USE [AdventureWorks2022]
GO

CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Strong Password';
GO

CREATE DATABASE SCOPED CREDENTIAL [CETASCredential]
    WITH IDENTITY = 'Managed Identity';
GO

CREATE EXTERNAL DATA SOURCE [CETASExternalDataSource]
WITH (
    LOCATION = 'abs://container@storageaccount.blob.core.windows.net',
    CREDENTIAL = [CETASCredential] );
GO

CREATE EXTERNAL FILE FORMAT [CETASFileFormat]
WITH(
    FORMAT_TYPE=PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
    );
GO

-- Count how many rows we plan to offload
SELECT COUNT(*) FROM [AdventureWorks2022].[Sales].[SalesOrderHeader] WHERE
        OrderDate < '2013-12-31';

-- CETAS write to a single file, archive all data older than 1-Jan-2014:
CREATE EXTERNAL TABLE SalesOrdersExternal
WITH (
    LOCATION = 'SalesOrders/',
    DATA_SOURCE = [CETASExternalDataSource],
    FILE_FORMAT = [CETASFileFormat])
AS 
    SELECT 
        *
    FROM 
        [AdventureWorks2022].[Sales].[SalesOrderHeader]
    WHERE
        OrderDate < '2013-12-31';

-- you can query the newly created external table
SELECT COUNT (*) FROM SalesOrdersExternal;