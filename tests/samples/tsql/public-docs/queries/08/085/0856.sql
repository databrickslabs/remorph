-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-assembly-transact-sql?view=sql-server-ver16

CREATE ASSEMBLY HelloWorld  
    FROM 0x4D5A900000000000  
WITH PERMISSION_SET = SAFE;