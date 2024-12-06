-- tsql sql:
WITH IndexCTE AS (
    SELECT 1 AS DropIndex
    WHERE EXISTS (
        SELECT 1
        FROM sys.indexes i
        INNER JOIN sys.tables t ON i.object_id = t.object_id
        WHERE i.name = N'PXML_Supplier_Address'
            AND t.name = N'Supplier'
            AND t.schema_id = SCHEMA_ID(N'Purchasing')
    )
)
SELECT CASE WHEN DropIndex = 1 THEN 'DROP INDEX PXML_Supplier_Address ON Purchasing.Supplier;' ELSE '' END AS Query
FROM IndexCTE;
