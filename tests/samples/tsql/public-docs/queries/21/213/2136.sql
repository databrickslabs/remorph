-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-full-text-permissions-transact-sql?view=sql-server-ver16

GRANT VIEW DEFINITION  
    ON FULLTEXT STOPLIST :: ProductStoplist  
    TO Mary ;