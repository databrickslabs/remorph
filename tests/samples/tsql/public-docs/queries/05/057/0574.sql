-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-external-data-source-transact-sql?view=sql-server-ver16

ALTER EXTERNAL DATA SOURCE AzureStorage_west SET
   LOCATION = 'wasbs://loadingdemodataset@updatedproductioncontainer.blob.core.windows.net',
   CREDENTIAL = AzureStorageCredential