--Query type: DCL
DECLARE @cookie VARBINARY(100);
DECLARE @current_user SYSNAME, @current_username SYSNAME;

EXECUTE AS USER = 'customer1' WITH COOKIE INTO @cookie;
SET @current_user = SUSER_NAME();
SET @current_username = USER_NAME();

REVERT;

SELECT 
    @current_user AS [current_user],
    @current_username AS current_username,
    'customer1' AS customer_name,
    'customer1_email' AS customer_email,
    'employee1' AS employee_name,
    'employee1_email' AS employee_email,
    @cookie AS cookie;