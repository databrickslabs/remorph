--Query type: DDL
DECLARE @NewColumnType nvarchar(50) = 'DECIMAL(5, 2);
EXECUTE ('ALTER TABLE dbo.doc_exy ALTER COLUMN column_a ' + @NewColumnType);
SELECT * FROM dbo.doc_exy;
