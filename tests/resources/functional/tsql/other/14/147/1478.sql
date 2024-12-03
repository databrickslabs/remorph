--Query type: DML
CREATE PROCEDURE usp_MyProcedure
AS
BEGIN
    DECLARE @MyCursor CURSOR;
    DECLARE @ID INT, @Name VARCHAR(50);
    SET @MyCursor = CURSOR FOR
    SELECT ID, Name FROM (VALUES (1, 'John'), (2, 'Doe'), (3, 'Jane')) AS MyTable(ID, Name);
    OPEN @MyCursor;
    FETCH NEXT FROM @MyCursor INTO @ID, @Name;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        PRINT 'ID: ' + CONVERT(VARCHAR, @ID) + ', Name: ' + @Name;
        FETCH NEXT FROM @MyCursor INTO @ID, @Name;
    END;
    CLOSE @MyCursor;
    DEALLOCATE @MyCursor;
END;

-- Execute the stored procedure
EXEC usp_MyProcedure;

-- Select from the table to show the data
SELECT * FROM (VALUES (1, 'John'), (2, 'Doe'), (3, 'Jane')) AS MyTable(ID, Name);

-- REMORPH CLEANUP: DROP PROCEDURE usp_MyProcedure;
