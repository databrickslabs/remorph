-- tsql sql:
SELECT 'DROP INDEX ' + IndexName + ' ON ' + TableName + ';' FROM (VALUES ('IX_Customer_Address', 'Customer'), ('IX_Supplier_Address', 'Supplier')) AS IndexesToDrop(IndexName, TableName);
