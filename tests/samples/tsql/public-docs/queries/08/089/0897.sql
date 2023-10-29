-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-column-master-key-transact-sql?view=sql-server-ver16

CREATE COLUMN MASTER KEY MyCMK  
WITH (  
    KEY_STORE_PROVIDER_NAME = 'CUSTOM_KEY_STORE',    
    KEY_PATH = 'https://contoso.vault/sales_db_tce_key'  
);