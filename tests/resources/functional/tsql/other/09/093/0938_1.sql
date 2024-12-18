-- tsql sql:
CREATE EXTERNAL DATA SOURCE [CustomerData]
WITH (
    LOCATION = 'wasbs://customerdata.dfs.core.windows.net/customerinfo/customerbaseoutputfolderpath',
    CREDENTIAL = [CustomerIdentity]
);
-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE [CustomerData];
