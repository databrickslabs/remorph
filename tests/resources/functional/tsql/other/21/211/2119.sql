-- tsql sql:
CREATE TABLE DemoTable (ID INT, Name VARCHAR(100));
INSERT INTO DemoTable (ID, Name) VALUES (1, 'Test');
WITH DemoCTE AS (
    SELECT ID, Name FROM DemoTable
)
SELECT * FROM DemoCTE;
GRANT SELECT ON DemoTable TO [YourDatabaseUsername];
SELECT * FROM DemoTable;
