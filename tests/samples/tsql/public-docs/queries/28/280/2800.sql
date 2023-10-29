-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/columns-updated-transact-sql?view=sql-server-ver16

SELECT TABLE_NAME, COLUMN_NAME,  
    COLUMNPROPERTY(OBJECT_ID(TABLE_SCHEMA + '.' + TABLE_NAME),  
    COLUMN_NAME, 'ColumnID') AS COLUMN_ID  
FROM AdventureWorks2022.INFORMATION_SCHEMA.COLUMNS  
WHERE TABLE_NAME = 'Person';