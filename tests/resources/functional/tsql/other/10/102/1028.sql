-- tsql sql:
WITH login_info AS (
    SELECT 'new_login_name' AS login_name, 'newStrongPasswordHere' AS password
)
SELECT 'CREATE LOGIN ' + login_name + ' WITH PASSWORD = ''' + password + ''';' AS query
FROM login_info;
