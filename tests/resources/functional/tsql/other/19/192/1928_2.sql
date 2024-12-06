-- tsql sql:
DECLARE @regionname nvarchar(25);
SELECT @regionname = 'Europe'
FROM (
    VALUES (1)
) AS temp_table(id);
