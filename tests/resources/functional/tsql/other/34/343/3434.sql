--Query type: DCL
WITH SchemaCollections AS (
    SELECT 'Sales.Invoices4' AS SchemaName
    UNION ALL
    SELECT 'dbo.Orders1'
    UNION ALL
    SELECT 'dbo.Orders2'
    UNION ALL
    SELECT 'dbo.Orders3'
)
SELECT SchemaName
FROM SchemaCollections;