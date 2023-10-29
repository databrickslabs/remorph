-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql?view=sql-server-ver16

EXEC sp_execute_external_script 
@language =N'R', 
@script=N'
# load the desired package packageA
library(packageA)
'