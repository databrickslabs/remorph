-- tsql sql:
WITH temp_result AS (SELECT 'sp_new_demo' AS proc_name, 'cert_new_demo' AS cert_name, 'nGFD4bb925DGvbd2439587y' AS password)
SELECT 'ADD SIGNATURE TO [' + proc_name + '] BY CERTIFICATE [' + cert_name + '] WITH PASSWORD = ''' + password + ''';'
FROM temp_result;

DECLARE @sql nvarchar(max);

SELECT @sql = 'ADD SIGNATURE TO [' + proc_name + '] BY CERTIFICATE [' + cert_name + '] WITH PASSWORD = ''' + password + ''';'
FROM temp_result;

EXEC sp_executesql @sql;

EXEC sp_new_demo;
