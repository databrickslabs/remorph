--Query type: DML
DECLARE @v2 sql_variant;
SET @v2 = 'XYZ';
SELECT @v2 AS Value, SQL_VARIANT_PROPERTY(@v2, 'BaseType') AS BaseType, SQL_VARIANT_PROPERTY(@v2, 'MaxLength') AS MaxLength
FROM (VALUES (1)) AS temp(id);