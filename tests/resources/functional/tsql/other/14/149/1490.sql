--Query type: DML
DECLARE @MyNewVariable INT;
SET @MyNewVariable = 2;
EXECUTE sp_executesql N'SELECT * FROM (VALUES (@MyNewVariable)) AS MyNewTable(MyNewColumn)';
