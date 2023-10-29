-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkconstraints-transact-sql?view=sql-server-ver16

SELECT <columns>
FROM <table_being_checked> LEFT JOIN <referenced_table>
    ON <table_being_checked.fkey1> = <referenced_table.pkey1>
    AND <table_being_checked.fkey2> = <referenced_table.pkey2>
WHERE <table_being_checked.fkey1> IS NOT NULL
    AND <referenced_table.pkey1> IS NULL
    AND <table_being_checked.fkey2> IS NOT NULL
    AND <referenced_table.pkey2> IS NULL;