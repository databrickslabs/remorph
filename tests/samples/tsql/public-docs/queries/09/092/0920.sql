-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE DATABASE SCOPED CREDENTIAL s3_dc
WITH
    IDENTITY = 'S3 Access Key', -- for S3-compatible object storage the identity must always be S3 Access Key
    SECRET = <access_key_id>:<secret_key_id> -- provided by the S3-compatible object storage
GO

CREATE EXTERNAL DATA SOURCE s3_ds
WITH
(   LOCATION = 's3://<ip_address>:<port>/'
,   CREDENTIAL = s3_dc
);
GO