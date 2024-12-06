-- tsql sql:
DECLARE @v1 sql_variant;
SET @v1 = 'ABC';

WITH temp AS (
    SELECT @v1 AS Value
)

SELECT Value, SQL_VARIANT_PROPERTY(Value, 'BaseType') AS BaseType, SQL_VARIANT_PROPERTY(Value, 'MaxLength') AS MaxLength
FROM temp;
