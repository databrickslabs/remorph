-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-language-transact-sql?view=sql-server-ver16

GRANT EXECUTE EXTERNAL SCRIPT ON EXTERNAL LANGUAGE ::Java 
TO mylogin;