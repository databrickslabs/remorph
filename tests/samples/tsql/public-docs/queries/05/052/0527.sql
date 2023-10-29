-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-scoped-configuration-transact-sql?view=sql-server-ver16

ALTER DATABASE SCOPED CONFIGURATION
SET LEDGER_DIGEST_STORAGE_ENDPOINT = 'https://mystorage.blob.core.windows.net'