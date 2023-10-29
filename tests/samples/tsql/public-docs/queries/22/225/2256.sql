-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

RESTORE DATABASE AdventureWorks2022
    FROM TAPE = '\\.\tape0';