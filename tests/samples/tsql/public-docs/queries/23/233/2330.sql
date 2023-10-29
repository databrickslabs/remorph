-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-function-sql-data-warehouse?view=aps-pdw-2016-au7

SELECT * 
FROM sys.objects o
CROSS APPLY dbo.ModulesByType(o.type);
GO