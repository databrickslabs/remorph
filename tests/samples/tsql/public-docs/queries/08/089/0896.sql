-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-column-master-key-transact-sql?view=sql-server-ver16

CREATE COLUMN MASTER KEY MyCMK  
WITH (  
     KEY_STORE_PROVIDER_NAME = N'MSSQL_CERTIFICATE_STORE',   
     KEY_PATH = 'Current User/Personal/f2260f28d909d21c642a3d8e0b45a830e79a1420'  
   );