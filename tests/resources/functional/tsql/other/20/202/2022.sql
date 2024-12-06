-- tsql sql:
WITH roles AS ( SELECT 'sales_team' AS role_name )
SELECT 'DROP SERVER ROLE ' + role_name + '; GO' AS query
FROM roles;
