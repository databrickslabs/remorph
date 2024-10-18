--Query type: DDL
CREATE EXTERNAL DATA SOURCE MyGoogleCloudStorage
WITH (
    TYPE = BLOB_STORAGE,
    LOCATION = 'https://****************.storage.googleapis.com/curriculum',
    CREDENTIAL = MyGoogleCloudStorageCredential
);
-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE MyGoogleCloudStorage;
-- REMORPH CLEANUP: DROP DATABASE SCOPED CREDENTIAL MyGoogleCloudStorageCredential;