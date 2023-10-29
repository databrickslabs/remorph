-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-file-format-transact-sql?view=sql-server-ver16

CREATE EXTERNAL FILE FORMAT DeltaFileFormat
WITH (
    FORMAT_TYPE = DELTA
);