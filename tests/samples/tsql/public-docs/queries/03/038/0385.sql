-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

--Blob Storage endpoint
abs://<container>@<storage_account>.blob.core.windows.net/<path>/<file_name>.parquet

--Data Lake endpoint
adls://<container>@<storage_account>.blob.core.windows.net/<path>/<file_name>.parquet