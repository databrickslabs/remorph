--Query type: DCL
CREATE TABLE #temp
(
    username nvarchar(50),
    password nvarchar(50)
);

INSERT INTO #temp (username, password)
VALUES ('JohnDoe', 'P@ssw0rd123!');

CREATE TABLE #sql_commands
(
    command nvarchar(max)
);

INSERT INTO #sql_commands (command)
SELECT 'CREATE LOGIN ' + username + ' WITH PASSWORD = ''' + password + ''';'
FROM #temp;

SELECT command
FROM #sql_commands;

-- REMORPH CLEANUP: DROP TABLE #temp;
-- REMORPH CLEANUP: DROP TABLE #sql_commands;
-- REMORPH CLEANUP: DROP LOGIN JohnDoe;