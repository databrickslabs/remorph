-- tsql sql:
CREATE TABLE MyFactTable (column1 INT);
CREATE INDEX IDX_CL_MyFactTable ON MyFactTable (column1);
DROP INDEX IDX_CL_MyFactTable ON MyFactTable;
SELECT * FROM (VALUES (1), (2), (3)) AS TemporaryResultSet(column1);
