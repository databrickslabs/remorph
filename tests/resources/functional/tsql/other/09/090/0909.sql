--Query type: DDL
CREATE DATABASE SCOPED CREDENTIAL AccessAzureOrders
WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
SECRET = '<azure_shared_access_signature>';

CREATE EXTERNAL DATA SOURCE MyAzureOrders
WITH (
    LOCATION = 'abs://<container>@<storage_account_name>.blob.core.windows.net/',
    CREDENTIAL = AccessAzureOrders
);

-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE MyAzureOrders;
-- REMORPH CLEANUP: DROP DATABASE SCOPED CREDENTIAL AccessAzureOrders;