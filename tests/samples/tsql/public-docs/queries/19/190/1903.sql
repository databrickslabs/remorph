-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/sql-variant-property-transact-sql?view=sql-server-ver16

DECLARE @v1 sql_variant;  
SET @v1 = 'ABC';  
SELECT @v1;  
SELECT SQL_VARIANT_PROPERTY(@v1, 'BaseType');  
SELECT SQL_VARIANT_PROPERTY(@v1, 'MaxLength');