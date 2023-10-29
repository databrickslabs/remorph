-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openrowset-transact-sql?view=sql-server-ver16

CREATE DATABASE SCOPED CREDENTIAL delta_storage_dsc   
WITH IDENTITY = 'SHARED ACCESS SIGNATURE', 
SECRET = '<SAS Token>';  

CREATE EXTERNAL DATA SOURCE Delta_ED
WITH
(
 LOCATION = 'adls://<container>@<storage_account>.dfs.core.windows.net'
,CREDENTIAL = delta_storage_dsc 
);

SELECT  * 
FROM    OPENROWSET
        (   BULK '/Contoso'
        ,   FORMAT = 'DELTA'
        ,   DATA_SOURCE = 'Delta_ED'
        ) as [result];