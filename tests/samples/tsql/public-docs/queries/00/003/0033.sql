-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

-- Create a database master key if one does not already exist, using your own password. This key is used to encrypt the credential secret in next step.
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<password>' ;
GO
CREATE DATABASE SCOPED CREDENTIAL AzureStorageCredentialv2
WITH
  IDENTITY = 'SHARED ACCESS SIGNATURE', -- to use SAS the identity must be fixed as-is
  SECRET = '<Blob_SAS_Token>' ;
GO
-- Create an external data source with CREDENTIAL option.
CREATE EXTERNAL DATA SOURCE MyAzureStorage
WITH
  ( LOCATION = 'abs://<container>@<storage_account_name>.blob.core.windows.net/' , 
    CREDENTIAL = AzureStorageCredentialv2,
  ) ;