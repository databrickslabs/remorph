--Query type: DQL
WITH temp_result AS (
    SELECT @@SPID AS 'ID',
           SYSTEM_USER AS 'Login Name',
           USER AS 'User Name'
)
SELECT 'Session ID' = ID,
       'Login Name' = [Login Name],
       'User Name' = [User Name]
FROM temp_result;