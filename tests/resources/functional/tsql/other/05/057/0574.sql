-- tsql sql:
WITH AzureStorage_east AS ( SELECT 'wasbs://loadingdemodataset@newproductioncontainer.blob.core.windows.net' AS LOCATION, 'AzureStorageCredential_east' AS CREDENTIAL ) SELECT LOCATION, CREDENTIAL FROM AzureStorage_east
