--Query type: DML
DECLARE @MyTable TABLE (MyID INT, MyName VARCHAR(50));
INSERT INTO @MyTable (MyID, MyName)
VALUES
    (1, 'John Doe'),
    (2, 'Jane Doe'),
    (3, 'Bob Smith');
UPDATE @MyTable
SET MyName = 'New Name'
WHERE MyID = 1;
SELECT *
FROM @MyTable;
