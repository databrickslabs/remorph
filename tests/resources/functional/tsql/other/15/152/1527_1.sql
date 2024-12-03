--Query type: TCL
DECLARE @session_id VARBINARY(100);
SET @session_id = (
    SELECT TOP 1 c_custkey
    FROM (
        VALUES (1, 'Customer#1'),
               (2, 'Customer#2')
    ) AS customers (c_custkey, c_name)
);
REVERT WITH COOKIE = @session_id;
SELECT SUSER_NAME(),
       USER_NAME();
