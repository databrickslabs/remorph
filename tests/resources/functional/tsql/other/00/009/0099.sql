--Query type: DDL
CREATE SEQUENCE customer_seq;
DECLARE @sql NVARCHAR(MAX) = (SELECT 'EXEC sp_rename ''' + seq_name + ''', ''' + 'customer_newseq' + ''', ''OBJECT''' FROM (VALUES ('customer_seq')) AS seq_name(seq_name));
EXEC sp_executesql @sql;
-- REMORPH CLEANUP: DROP SEQUENCE customer_newseq;