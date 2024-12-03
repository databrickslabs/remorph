--Query type: DCL
CREATE LOGIN newlogin WITH PASSWORD = 'Another Strong Pwd456!';
EXEC sp_addsrvrolemember 'newlogin', 'dbcreator';

WITH temp_result AS (
    SELECT 'newlogin' AS login_name, 'CREATE ANY DATABASE' AS privilege
)
SELECT *
FROM temp_result;

-- REMORPH CLEANUP: DROP LOGIN newlogin;
