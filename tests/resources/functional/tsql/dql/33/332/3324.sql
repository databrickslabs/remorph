-- tsql sql:
WITH temp_result AS (SELECT 'HelloWorld' AS assembly_name)
SELECT ASSEMBLYPROPERTY(assembly_name, 'PublicKey')
FROM temp_result
