-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-external-library-transact-sql?view=sql-server-ver16

EXEC sp_execute_external_script 
@language =N'R', 
@script=N'library(customPackage)'
;