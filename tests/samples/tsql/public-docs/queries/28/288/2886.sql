-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-function-sql-data-warehouse?view=aps-pdw-2016-au7

SELECT definition, type   
FROM sys.sql_modules AS m  
JOIN sys.objects AS o   
    ON m.object_id = o.object_id   
    AND type = ('FN');  
GO