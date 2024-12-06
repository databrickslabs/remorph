-- tsql sql:
CREATE DATABASE SCOPED CREDENTIAL AccessAzureOrders
WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
SECRET = '<azure_shared_access_signature>';

CREATE EXTERNAL DATA SOURCE MyAzureOrders
WITH (
LOCATION = 'https://neworders.blob.core.windows.net/week4',
CREDENTIAL = AccessAzureOrders,
TYPE = BLOB_STORAGE
);

-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE MyAzureOrders;
-- REMORPH CLEANUP: DROP DATABASE SCOPED CREDENTIAL AccessAzureOrders;
