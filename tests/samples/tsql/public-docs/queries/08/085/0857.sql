-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-assembly-transact-sql?view=sql-server-ver16

CREATE ASSEMBLY HelloWorld   
FROM '<system_drive>:\Program Files\Microsoft SQL Server\100\Samples\HelloWorld\CS\HelloWorld\bin\debug\HelloWorld.dll'  
WITH PERMISSION_SET = SAFE;