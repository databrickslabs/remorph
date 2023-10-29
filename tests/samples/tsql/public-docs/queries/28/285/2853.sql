-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

SELECT [name], [value] FROM sys.configurations WHERE name ='allow polybase export';