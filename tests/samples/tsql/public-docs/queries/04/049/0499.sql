-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-column-encryption-key-transact-sql?view=sql-server-ver16

ALTER COLUMN ENCRYPTION KEY MyCEK  
DROP VALUE  
(  
    COLUMN_MASTER_KEY = MyCMK  
);  
GO