--Query type: DCL
DECLARE @sql NVARCHAR(MAX) = '';

WITH objects AS
(
    SELECT 'customer' AS object_name
    UNION ALL
    SELECT 'orders'
    UNION ALL
    SELECT 'lineitem'
    UNION ALL
    SELECT 'part'
    UNION ALL
    SELECT 'supplier'
    UNION ALL
    SELECT 'partsupp'
    UNION ALL
    SELECT 'nation'
    UNION ALL
    SELECT 'region'
)

SELECT @sql += 'ALTER AUTHORIZATION ON OBJECT::' + object_name + ' TO MichikoOsada;' + CHAR(13) + CHAR(10)
FROM objects;

EXEC sp_executesql @sql;
