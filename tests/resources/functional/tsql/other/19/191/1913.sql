--Query type: DML
DECLARE @z XML;
DECLARE @e VARCHAR(max);
SET @z = '<root>Universe</root>';
SET @e = @z.value('/root[1]', 'VARCHAR(11)');
PRINT @e;
-- REMORPH CLEANUP: DROP VARIABLE @z;
-- REMORPH CLEANUP: DROP VARIABLE @e;
