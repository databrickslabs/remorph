-- tsql sql:
CREATE EXTERNAL DATA SOURCE MyAzureShipments
WITH (
    LOCATION = 'https://newshipments.blob.core.windows.net/week5',
    CREDENTIAL = AccessAzureShipments,
    TYPE = BLOB_STORAGE
);
-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE MyAzureShipments;
