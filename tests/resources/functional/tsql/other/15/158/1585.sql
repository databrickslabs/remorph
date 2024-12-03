--Query type: DML
DECLARE @db_name sysname;
DECLARE @file_path nvarchar(400);

WITH DatabaseBackups AS (
    SELECT 'MyDatabase' AS db_name, 'C:\MyBackups\MyDatabase.bak' AS file_path
)

SELECT @db_name = db_name, @file_path = file_path
FROM DatabaseBackups
WHERE db_name = 'MyDatabase';

CREATE TABLE #DatabaseBackups (
    db_name sysname,
    file_path nvarchar(400)
);

INSERT INTO #DatabaseBackups (db_name, file_path)
VALUES ('MyDatabase', 'C:\MyBackups\MyDatabase.bak');

SELECT * FROM #DatabaseBackups;

-- REMORPH CLEANUP: DROP TABLE #DatabaseBackups;
