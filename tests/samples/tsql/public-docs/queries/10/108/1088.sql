-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql?view=sql-server-ver16

CREATE PROCEDURE dbo.InsertUnitMeasure @UnitMeasureCode NCHAR(3),
    @Name NVARCHAR(25)
AS
BEGIN
    SET NOCOUNT ON;

    -- Update the row if it exists.
    UPDATE Production.UnitMeasure
    SET Name = @Name
    WHERE UnitMeasureCode = @UnitMeasureCode

    -- Insert the row if the UPDATE statement failed.
    IF (@@ROWCOUNT = 0)
    BEGIN
        INSERT INTO Production.UnitMeasure (
            UnitMeasureCode,
            Name
        )
        VALUES (@UnitMeasureCode, @Name)
    END
END;
GO

-- Test the procedure and return the results.
EXEC InsertUnitMeasure @UnitMeasureCode = 'ABC', @Name = 'Test Value';

SELECT UnitMeasureCode, Name
FROM Production.UnitMeasure
WHERE UnitMeasureCode = 'ABC';
GO

-- Rewrite the procedure to perform the same operations using the
-- MERGE statement.
ALTER PROCEDURE dbo.InsertUnitMeasure @UnitMeasureCode NCHAR(3),
    @Name NVARCHAR(25)
AS
BEGIN
    SET NOCOUNT ON;

    MERGE Production.UnitMeasure AS tgt
    USING (
        SELECT @UnitMeasureCode,
            @Name
        ) AS src(UnitMeasureCode, Name)
        ON (tgt.UnitMeasureCode = src.UnitMeasureCode)
    WHEN MATCHED
        THEN
            UPDATE SET Name = src.Name
    WHEN NOT MATCHED
        THEN
            INSERT (UnitMeasureCode, Name)
            VALUES (src.UnitMeasureCode, src.Name);
END;
GO

-- Test the procedure and return the results.
EXEC InsertUnitMeasure @UnitMeasureCode = 'ABC', @Name = 'New Test Value';
EXEC InsertUnitMeasure @UnitMeasureCode = 'XYZ', @Name = 'Test Value';
EXEC InsertUnitMeasure @UnitMeasureCode = 'ABC', @Name = 'Another Test Value';

-- Cleanup
DELETE FROM Production.UnitMeasure
WHERE UnitMeasureCode IN ('ABC', 'XYZ');
GO