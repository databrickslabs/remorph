-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openrowset-transact-sql?view=sql-server-ver16

CREATE DATABASE SCOPED CREDENTIAL s3_dsc
WITH IDENTITY = 'S3 Access Key',
SECRET = 'contosoadmin:contosopwd'
GO

CREATE EXTERNAL DATA SOURCE s3_eds
WITH
(
 LOCATION = 's3://10.199.40.235:9000/movies'
,CREDENTIAL = s3_dsc
)
GO

SELECT *
FROM  
    OPENROWSET(
        BULK (
            '/decades/1950s/*.parquet',
			'/decades/1960s/*.parquet',
			'/decades/1970s/*.parquet'),
        FORMAT='PARQUET'
		,DATA_SOURCE = 's3_eds'
    )
AS [data]