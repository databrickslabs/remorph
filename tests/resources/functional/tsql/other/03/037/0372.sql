--Query type: DDL
WITH tables_to_rename AS (
    SELECT 'DimCustomer' AS old_name, 'DimCustomer_old' AS new_name
    UNION ALL
    SELECT 'myTable', 'DimCustomer'
)
SELECT 'RENAME OBJECT [dbo].[' + old_name + '] to [' + new_name + '];' AS rename_query
FROM tables_to_rename;