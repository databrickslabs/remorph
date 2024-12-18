-- tsql sql:
DECLARE @query nvarchar(max);
DECLARE @schema_name nvarchar(50);
DECLARE @table_name nvarchar(50);
DECLARE @name nvarchar(50);
DECLARE @result TABLE (name nvarchar(50));
INSERT INTO @result
SELECT name
FROM (VALUES ('NewTitle', 'joe', 'titles')) AS temp_result (name, schema_name, table_name)
WHERE name = 'NewTitle';
SELECT * FROM @result;
-- REMORPH CLEANUP: DROP TABLE @result;
