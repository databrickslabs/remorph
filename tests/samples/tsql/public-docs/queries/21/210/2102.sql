-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql?view=sql-server-ver16

EXECUTE sp_execute_external_script 
    @LANGUAGE = N'R',
    @SCRIPT = N'
library(packageA)'