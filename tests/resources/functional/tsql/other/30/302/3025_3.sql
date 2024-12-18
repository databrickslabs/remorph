-- tsql sql:
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ExampleTable')
CREATE TABLE ExampleTable (
    ID INT,
    Text NVARCHAR(MAX)
);

INSERT INTO ExampleTable (ID, Text)
SELECT ID, Text
FROM (
    VALUES
        (1, 'Text in single quotes'),
        (2, 'Text in single quotes'),
        (3, 'Text with 2 '' single quotes'),
        (4, 'Text in double quotes'),
        (5, 'Text in double quotes'),
        (6, 'Text with 2 " double quotes')
) AS Data(ID, Text);

SELECT * FROM ExampleTable;

-- REMORPH CLEANUP: DROP TABLE ExampleTable;
