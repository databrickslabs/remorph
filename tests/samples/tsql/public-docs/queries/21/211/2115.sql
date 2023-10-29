-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-full-text-permissions-transact-sql?view=sql-server-ver16

GRANT CONTROL  
    ON FULLTEXT CATALOG :: ProductCatalog  
    TO Ted ;