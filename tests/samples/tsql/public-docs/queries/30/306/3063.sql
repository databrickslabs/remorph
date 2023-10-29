-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinklog-azure-sql-data-warehouse?view=aps-pdw-2016-au7

USE Addresses;
GO
DBCC SHRINKLOG ( SIZE = 100 MB );
GO
DBCC SHRINKLOG ( SIZE = DEFAULT );
GO
DBCC SHRINKLOG;
GO