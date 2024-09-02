--Query type: DDL
WITH IndexCTE AS (
    SELECT 'PXML_Supplier_Address' AS IndexName
),
CheckIndexCTE AS (
    SELECT CASE WHEN EXISTS (
            SELECT 1
            FROM IndexCTE
            WHERE IndexName = 'PXML_Supplier_Address'
        ) THEN 1 ELSE 0 END AS IndexExists
)
SELECT CASE WHEN IndexExists = 1 THEN 'DROP INDEX PXML_Supplier_Address ON Purchasing.Supplier;' ELSE '' END AS Query
FROM CheckIndexCTE;