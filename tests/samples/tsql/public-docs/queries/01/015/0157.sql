-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

-- This database RESTORE halted prematurely due to power failure.
RESTORE DATABASE AdventureWorks2022
    FROM AdventureWorksBackups;
-- Here is the RESTORE RESTART operation.
RESTORE DATABASE AdventureWorks2022
    FROM AdventureWorksBackups WITH RESTART;