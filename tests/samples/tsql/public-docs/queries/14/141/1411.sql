-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-show-statistics-transact-sql?view=sql-server-ver16

DBCC SHOW_STATISTICS ("Person.Address", AK_Address_rowguid);
GO