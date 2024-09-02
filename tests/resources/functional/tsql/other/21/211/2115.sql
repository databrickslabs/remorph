--Query type: DCL
WITH CatalogUsers AS (
    SELECT 'CustomerCatalog' AS CatalogName, 'Manager' AS UserName
)
SELECT 'GRANT CONTROL ON FULLTEXT CATALOG :: ' + CatalogName + ' TO ' + UserName + ';' AS GrantStatement
FROM CatalogUsers;