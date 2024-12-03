--Query type: DDL
CREATE EXTERNAL DATA SOURCE [AzureDataLakeStorage]
WITH (
    LOCATION = 'https://mydatalakestorage.dfs.core.windows.net/mycontainer/myoutputfolderpath',
    CREDENTIAL = [MyWorkspaceCredential]
);
-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE [AzureDataLakeStorage];
-- REMORPH CLEANUP: DROP DATABASE SCOPED CREDENTIAL [MyWorkspaceCredential];
