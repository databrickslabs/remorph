-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

SELECT  *
FROM    OPENROWSET
        (   BULK '/<bucket>/<parquet_folder>'
        ,   FORMAT       = 'PARQUET'
        ,   DATA_SOURCE  = 's3_ds'
        ) AS [cc];