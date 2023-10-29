-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-search-property-list-transact-sql?view=sql-server-ver16

SELECT column_name  
FROM table_name  
WHERE CONTAINS( PROPERTY( column_name, 'new_search_property' ), 
               'contains_search_condition');  
GO